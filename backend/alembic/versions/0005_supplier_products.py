"""supplier products and stock balance indexes

Revision ID: 0005_supplier_products
Revises: 0004_inventory_audit_models
Create Date: 2026-03-07 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0005_supplier_products"
down_revision = "0004_inventory_audit_models"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "supplier_products",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("supplier_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("unit_cost", sa.Numeric(14, 4)),
        sa.ForeignKeyConstraint(["supplier_id"], ["suppliers.id"]),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.UniqueConstraint("supplier_id", "product_id"),
    )

    op.create_index(
        "uq_stock_balance_null_lot",
        "stock_balance",
        ["product_id", "location_id"],
        unique=True,
        postgresql_where=sa.text("lot_id IS NULL"),
    )
    op.create_index(
        "uq_stock_balance_with_lot",
        "stock_balance",
        ["product_id", "location_id", "lot_id"],
        unique=True,
        postgresql_where=sa.text("lot_id IS NOT NULL"),
    )


def downgrade() -> None:
    op.drop_index("uq_stock_balance_with_lot", table_name="stock_balance")
    op.drop_index("uq_stock_balance_null_lot", table_name="stock_balance")
    op.drop_table("supplier_products")
