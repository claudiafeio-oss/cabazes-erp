from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base


class AssemblyOrder(Base):
    __tablename__ = "assembly_orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    basket_product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"), nullable=False
    )
    basket_bom_id: Mapped[int | None] = mapped_column(ForeignKey("basket_boms.id"))
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    planned_quantity: Mapped[float] = mapped_column(Numeric(14, 3), nullable=False)
    produced_quantity: Mapped[float] = mapped_column(Numeric(14, 3), nullable=False, default=0)
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    basket_product = relationship("Product")
    basket_bom = relationship("BasketBom")
    planned_lines = relationship("AssemblyOrderPlannedLine", back_populates="assembly_order")
    consumption_lines = relationship(
        "AssemblyOrderConsumptionLine", back_populates="assembly_order"
    )
    output_lines = relationship("AssemblyOrderOutputLine", back_populates="assembly_order")
