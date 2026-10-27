from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_current_admin, get_current_user, get_db
from app.models.user import User, UserRole
from app.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate
from app.services.order import OrderService

orders_router = APIRouter(prefix="/orders", tags=["Orders"])

@orders_router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order_in: OrderCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    order_service = OrderService(db)
    return await order_service.create_order(user_id=current_user.id, order_in=order_in)

@orders_router.get("", response_model=list[OrderResponse])
async def list_orders(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    order_service = OrderService(db)
    if current_user.role == UserRole.ADMIN:
        return await order_service.get_all_orders()
    return await order_service.get_user_orders(user_id=current_user.id)

@orders_router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    order_service = OrderService(db)
    is_admin = current_user.role == UserRole.ADMIN
    return await order_service.get_order_by_id(order_id=order_id, user_id=current_user.id, is_admin=is_admin)

@orders_router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(order_id: int, status_in: OrderStatusUpdate, db: AsyncSession = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    order_service = OrderService(db)
    return await order_service.update_order_status(order_id=order_id, status_in=status_in)