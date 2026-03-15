from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base


class BasketBom(Base):
    __tablename__ = "basket_boms"

    id: Mapped[int] = mapped_column(primary_key=True)
    basket_product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"), nullable=False
    )
    version: Mapped[str] = mapped_column(String(32), nullable=False, default="v1")
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    basket_product = relationship("Product")
    lines = relationship("BasketBomLine", back_populates="basket_bom")
