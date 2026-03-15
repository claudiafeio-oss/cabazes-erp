from sqlalchemy import Boolean, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class Product(Base, TimestampMixin):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    product_type: Mapped[str] = mapped_column(String(32), nullable=False)
    unit_of_measure: Mapped[str] = mapped_column(String(32), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    track_lot: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    track_expiry: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    minimum_stock: Mapped[float] = mapped_column(Numeric(14, 3), nullable=False, default=0)
    default_cost: Mapped[float] = mapped_column(Numeric(14, 4), nullable=False, default=0)

    lots = relationship("Lot", back_populates="product")
    stock_moves = relationship("StockMove", back_populates="product")
    stock_balances = relationship("StockBalance", back_populates="product")
    supplier_products = relationship("SupplierProduct", back_populates="product")
