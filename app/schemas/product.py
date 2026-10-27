from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict

class ProductBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    price: Decimal = Field(..., gt=0, decimal_places=2)
    stock: int = Field(default=0, ge=0)
    is_available: bool = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    price: Decimal | None = Field(None, gt=0, decimal_places=2)
    stock: int | None = Field(None, ge=0)
    is_available: bool | None = None

class ProductResponse(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)