from datetime import date

from sqlalchemy import Date, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class AssemblyOrderOutputLine(Base):
    __tablename__ = "assembly_order_output_lines"

    id: Mapped[int] = mapped_column(primary_key=True)
    assembly_order_id: Mapped[int] = mapped_column(
        ForeignKey("assembly_orders.id"), nullable=False
    )
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    lot_id: Mapped[int | None] = mapped_column(ForeignKey("lots.id"))
    quantity_produced: Mapped[float] = mapped_column(Numeric(14, 3), nullable=False)
    expiry_date: Mapped[date | None] = mapped_column(Date)

    assembly_order = relationship("AssemblyOrder", back_populates="output_lines")
    product = relationship("Product")
    lot = relationship("Lot")
