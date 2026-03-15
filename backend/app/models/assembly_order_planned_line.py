from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class AssemblyOrderPlannedLine(Base):
    __tablename__ = "assembly_order_planned_lines"

    id: Mapped[int] = mapped_column(primary_key=True)
    assembly_order_id: Mapped[int] = mapped_column(
        ForeignKey("assembly_orders.id"), nullable=False
    )
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity_planned: Mapped[float] = mapped_column(Numeric(14, 3), nullable=False)
    substitution_group_id: Mapped[int | None] = mapped_column(
        ForeignKey("substitution_groups.id")
    )

    assembly_order = relationship("AssemblyOrder", back_populates="planned_lines")
    product = relationship("Product")
    substitution_group = relationship("SubstitutionGroup")
