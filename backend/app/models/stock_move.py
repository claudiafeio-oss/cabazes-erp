from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base


class StockMove(Base):
    __tablename__ = "stock_moves"
    __table_args__ = (
        Index("ix_stock_moves_product_location", "product_id", "location_id"),
        Index("ix_stock_moves_lot", "lot_id"),
        Index("ix_stock_moves_occurred_at", "occurred_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"), nullable=False)
    lot_id: Mapped[int | None] = mapped_column(ForeignKey("lots.id"))
    quantity: Mapped[float] = mapped_column(Numeric(14, 3), nullable=False)
    move_type: Mapped[str] = mapped_column(String(32), nullable=False)
    reference_type: Mapped[str | None] = mapped_column(String(32))
    reference_id: Mapped[int | None] = mapped_column()
    unit_cost: Mapped[float | None] = mapped_column(Numeric(14, 4))
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    product = relationship("Product", back_populates="stock_moves")
    location = relationship("Location", back_populates="stock_moves")
    lot = relationship("Lot", back_populates="stock_moves")
