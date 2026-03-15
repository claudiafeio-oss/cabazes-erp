from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class SubstitutionGroupItem(Base):
    __tablename__ = "substitution_group_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    substitution_group_id: Mapped[int] = mapped_column(
        ForeignKey("substitution_groups.id"), nullable=False
    )
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)

    group = relationship("SubstitutionGroup", back_populates="items")
    product = relationship("Product")
