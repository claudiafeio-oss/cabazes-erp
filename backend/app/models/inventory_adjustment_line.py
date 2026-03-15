from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class InventoryAdjustmentLine(Base):
    __tablename__ = "inventory_adjustment_lines"

    id: Mapped[int] = mapped_column(primary_key=True)
    adjustment_id: Mapped[int] = mapped_column(
        ForeignKey("inventory_adjustments.id"), nullable=False
    )
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    lot_id: Mapped[int | None] = mapped_column(ForeignKey("lots.id"))
    quantity_counted: Mapped[float] = mapped_column(Numeric(14, 3), nullable=False)
    quantity_system: Mapped[float] = mapped_column(Numeric(14, 3), nullable=False)
    quantity_difference: Mapped[float] = mapped_column(Numeric(14, 3), nullable=False)

    adjustment = relationship("InventoryAdjustment", back_populates="lines")
    product = relationship("Product")
    lot = relationship("Lot")
