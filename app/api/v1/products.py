from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_current_admin, get_db
from app.models.user import User
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.services.product import ProductService

products_router = APIRouter(prefix="/products", tags=["Products"])

@products_router.get("", response_model=list[ProductResponse])
async def list_products(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=100), db: AsyncSession = Depends(get_db)):
    product_service = ProductService(db)
    return await product_service.get_products(skip=skip, limit=limit)

@products_router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product_service = ProductService(db)
    return await product_service.get_product_by_id(product_id)

@products_router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product_in: ProductCreate, db: AsyncSession = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    product_service = ProductService(db)
    return await product_service.create_product(product_in)


@products_router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product_in: ProductUpdate, db: AsyncSession = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    product_service = ProductService(db)
    return await product_service.update_product(product_id, product_in)

@products_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    product_service = ProductService(db)
    await product_service.delete_product(product_id)