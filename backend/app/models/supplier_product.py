from sqlalchemy import ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class SupplierProduct(Base):
    __tablename__ = "supplier_products"
    __table_args__ = (UniqueConstraint("supplier_id", "product_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    unit_cost: Mapped[float | None] = mapped_column(Numeric(14, 4))

    supplier = relationship("Supplier", back_populates="products")
    product = relationship("Product", back_populates="supplier_products")
