from datetime import date

from sqlalchemy import Date, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class Lot(Base, TimestampMixin):
    __tablename__ = "lots"
    __table_args__ = (UniqueConstraint("product_id", "lot_code"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    lot_code: Mapped[str] = mapped_column(String(64), nullable=False)
    expiry_date: Mapped[date | None] = mapped_column(Date)

    product = relationship("Product", back_populates="lots")
    stock_moves = relationship("StockMove", back_populates="lot")
    stock_balances = relationship("StockBalance", back_populates="lot")
