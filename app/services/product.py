from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

class ProductService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_product(self, product_in: ProductCreate) -> Product:
        product = Product(**product_in.model_dump())
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def get_products(self, skip: int = 0, limit: int = 100) -> list[Product]:
        result = await self.db.execute(select(Product).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def get_product_by_id(self, product_id: int) -> Product:
        result = await self.db.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )
        return product

    async def update_product(self, product_id: int, product_in: ProductUpdate) -> Product:
        product = await self.get_product_by_id(product_id)
        update_data = product_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def delete_product(self, product_id: int) -> None:
        product = await self.get_product_by_id(product_id)
        await self.db.delete(product)
        await self.db.commit()