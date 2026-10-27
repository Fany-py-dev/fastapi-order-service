from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderStatusUpdate

class OrderService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_order(self, user_id: int, order_in: OrderCreate) -> Order:
        total_amount = 0
        order_items_to_create = []
        for item in order_in.items:
            result = await self.db.execute(select(Product).where(Product.id == item.product_id))
            product = result.scalar_one_or_none()

            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with id {item.product_id} not found",
                )

            if not product.is_available:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Product '{product.title}' is currently unavailable",
                )

            if product.stock < item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Not enough stock for product '{product.title}'. Requested: {item.quantity}, Available: {product.stock}",
                )

            product.stock -= item.quantity
            self.db.add(product)
            item_price = product.price * item.quantity
            total_amount += item_price
            order_item = OrderItem(product_id=product.id, quantity=item.quantity, price_at_purchase=product.price)
            order_items_to_create.append(order_item)

        order = Order(user_id=user_id, status=OrderStatus.PENDING, total_amount=total_amount, items=order_items_to_create)
        self.db.add(order)
        await self.db.commit()
        return await self.get_order_by_id(order.id, user_id=user_id, is_admin=False)

    async def get_user_orders(self, user_id: int) -> list[Order]:
        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.items).selectinload(OrderItem.product))
            .where(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_all_orders(self) -> list[Order]:
        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.items).selectinload(OrderItem.product))
            .order_by(Order.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_order_by_id(self, order_id: int, user_id: int, is_admin: bool = False) -> Order:
        stmt = (
            select(Order)
            .options(selectinload(Order.items).selectinload(OrderItem.product))
            .where(Order.id == order_id)
        )
        if not is_admin:
            stmt = stmt.where(Order.user_id == user_id)
        result = await self.db.execute(stmt)
        order = result.scalar_one_or_none()

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )
        return order

    async def update_order_status(self, order_id: int, status_in: OrderStatusUpdate) -> Order:
        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.items).selectinload(OrderItem.product))
            .where(Order.id == order_id)
        )
        order = result.scalar_one_or_none()

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )

        order.status = status_in.status
        self.db.add(order)
        await self.db.commit()
        await self.db.refresh(order)
        return order