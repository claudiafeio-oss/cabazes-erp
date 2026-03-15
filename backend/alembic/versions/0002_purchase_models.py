"""purchase models

Revision ID: 0002_purchase_models
Revises: 0001_core_models
Create Date: 2026-03-07 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0002_purchase_models"
down_revision = "0001_core_models"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "purchase_orders",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("supplier_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column(
            "ordered_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("confirmed_at", sa.DateTime(timezone=True)),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(["supplier_id"], ["suppliers.id"]),
    )
    op.create_table(
        "purchase_order_lines",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("purchase_order_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("quantity_ordered", sa.Numeric(14, 3), nullable=False),
        sa.Column("unit_cost", sa.Numeric(14, 4)),
        sa.ForeignKeyConstraint(["purchase_order_id"], ["purchase_orders.id"]),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
    )
    op.create_table(
        "purchase_receipts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("purchase_order_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("received_at", sa.DateTime(timezone=True)),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(["purchase_order_id"], ["purchase_orders.id"]),
    )
    op.create_table(
        "purchase_receipt_lines",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("receipt_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("location_id", sa.Integer(), nullable=False),
        sa.Column("lot_id", sa.Integer()),
        sa.Column("expiry_date", sa.Date()),
        sa.Column("quantity_received", sa.Numeric(14, 3), nullable=False),
        sa.Column("unit_cost", sa.Numeric(14, 4)),
        sa.ForeignKeyConstraint(["receipt_id"], ["purchase_receipts.id"]),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.ForeignKeyConstraint(["location_id"], ["locations.id"]),
        sa.ForeignKeyConstraint(["lot_id"], ["lots.id"]),
    )


def downgrade() -> None:
    op.drop_table("purchase_receipt_lines")
    op.drop_table("purchase_receipts")
    op.drop_table("purchase_order_lines")
    op.drop_table("purchase_orders")
