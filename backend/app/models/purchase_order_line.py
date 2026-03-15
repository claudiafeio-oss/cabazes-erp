from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class PurchaseOrderLine(Base):
    __tablename__ = "purchase_order_lines"

    id: Mapped[int] = mapped_column(primary_key=True)
    purchase_order_id: Mapped[int] = mapped_column(
        ForeignKey("purchase_orders.id"), nullable=False
    )
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity_ordered: Mapped[float] = mapped_column(Numeric(14, 3), nullable=False)
    unit_cost: Mapped[float | None] = mapped_column(Numeric(14, 4))

    purchase_order = relationship("PurchaseOrder", back_populates="lines")
    product = relationship("Product")
