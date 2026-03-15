from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class SubstitutionGroup(Base, TimestampMixin):
    __tablename__ = "substitution_groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    items = relationship("SubstitutionGroupItem", back_populates="group")
    bom_lines = relationship("BasketBomLine", back_populates="substitution_group")
