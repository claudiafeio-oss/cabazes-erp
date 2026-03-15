from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base


class PurchaseReceipt(Base):
    __tablename__ = "purchase_receipts"

    id: Mapped[int] = mapped_column(primary_key=True)
    purchase_order_id: Mapped[int] = mapped_column(
        ForeignKey("purchase_orders.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    received_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    purchase_order = relationship("PurchaseOrder", back_populates="receipts")
    lines = relationship("PurchaseReceiptLine", back_populates="receipt")
