from decimal import Decimal
from typing import List, TYPE_CHECKING
from sqlalchemy import String, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.order import OrderItem

class Product(Base):
    __tablename__ = "products"
    title: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(default=0, nullable=False)
    is_available: Mapped[bool] = mapped_column(default=True, nullable=False)
    order_items: Mapped[List["OrderItem"]] = relationship(back_populates="product")