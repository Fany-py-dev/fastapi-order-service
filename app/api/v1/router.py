from fastapi import APIRouter
from app.api.v1.auth import auth_router
from app.api.v1.products import products_router
from app.api.v1.orders import orders_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(products_router)
api_router.include_router(orders_router)