from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict
from app.models.order import OrderStatus
from app.schemas.product import ProductResponse

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)

class OrderCreate(BaseModel):
    items: list[OrderItemCreate] = Field(..., min_length=1)

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price_at_purchase: Decimal
    product: ProductResponse
    model_config = ConfigDict(from_attributes=True)

class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: OrderStatus
    total_amount: Decimal
    created_at: datetime
    items: list[OrderItemResponse]
    model_config = ConfigDict(from_attributes=True)

class OrderStatusUpdate(BaseModel):
    status: OrderStatus