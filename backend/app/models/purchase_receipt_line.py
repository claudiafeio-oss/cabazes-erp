from datetime import date

from sqlalchemy import Date, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class PurchaseReceiptLine(Base):
    __tablename__ = "purchase_receipt_lines"

    id: Mapped[int] = mapped_column(primary_key=True)
    receipt_id: Mapped[int] = mapped_column(
        ForeignKey("purchase_receipts.id"), nullable=False
    )
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    location_id: Mapped[int] = mapped_column(
        ForeignKey("locations.id"), nullable=False
    )
    lot_id: Mapped[int | None] = mapped_column(ForeignKey("lots.id"))
    expiry_date: Mapped[date | None] = mapped_column(Date)
    quantity_received: Mapped[float] = mapped_column(Numeric(14, 3), nullable=False)
    unit_cost: Mapped[float | None] = mapped_column(Numeric(14, 4))

    receipt = relationship("PurchaseReceipt", back_populates="lines")
    product = relationship("Product")
    location = relationship("Location")
    lot = relationship("Lot")
