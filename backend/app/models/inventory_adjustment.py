from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base


class InventoryAdjustment(Base):
    __tablename__ = "inventory_adjustments"

    id: Mapped[int] = mapped_column(primary_key=True)
    location_id: Mapped[int] = mapped_column(
        ForeignKey("locations.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    counted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    location = relationship("Location")
    lines = relationship("InventoryAdjustmentLine", back_populates="adjustment")
