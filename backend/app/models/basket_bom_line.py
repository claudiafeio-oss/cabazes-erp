from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class BasketBomLine(Base):
    __tablename__ = "basket_bom_lines"

    id: Mapped[int] = mapped_column(primary_key=True)
    basket_bom_id: Mapped[int] = mapped_column(
        ForeignKey("basket_boms.id"), nullable=False
    )
    component_product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"), nullable=False
    )
    quantity: Mapped[float] = mapped_column(Numeric(14, 3), nullable=False)
    substitution_group_id: Mapped[int | None] = mapped_column(
        ForeignKey("substitution_groups.id")
    )

    basket_bom = relationship("BasketBom", back_populates="lines")
    component_product = relationship("Product")
    substitution_group = relationship("SubstitutionGroup", back_populates="bom_lines")
