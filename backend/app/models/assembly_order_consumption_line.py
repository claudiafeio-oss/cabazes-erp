from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class AssemblyOrderConsumptionLine(Base):
    __tablename__ = "assembly_order_consumption_lines"

    id: Mapped[int] = mapped_column(primary_key=True)
    assembly_order_id: Mapped[int] = mapped_column(
        ForeignKey("assembly_orders.id"), nullable=False
    )
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    lot_id: Mapped[int | None] = mapped_column(ForeignKey("lots.id"))
    quantity_consumed: Mapped[float] = mapped_column(Numeric(14, 3), nullable=False)
    planned_product_id: Mapped[int | None] = mapped_column(
        ForeignKey("products.id")
    )
    substitution_group_id: Mapped[int | None] = mapped_column(
        ForeignKey("substitution_groups.id")
    )

    assembly_order = relationship("AssemblyOrder", back_populates="consumption_lines")
    product = relationship("Product", foreign_keys=[product_id])
    planned_product = relationship("Product", foreign_keys=[planned_product_id])
    lot = relationship("Lot")
    substitution_group = relationship("SubstitutionGroup")
