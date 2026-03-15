from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base


class StockBalance(Base):
    __tablename__ = "stock_balance"
    __table_args__ = (
        UniqueConstraint("product_id", "location_id", "lot_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"), nullable=False)
    lot_id: Mapped[int | None] = mapped_column(ForeignKey("lots.id"))
    quantity: Mapped[float] = mapped_column(Numeric(14, 3), nullable=False, default=0)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    product = relationship("Product", back_populates="stock_balances")
    location = relationship("Location", back_populates="stock_balances")
    lot = relationship("Lot", back_populates="stock_balances")
