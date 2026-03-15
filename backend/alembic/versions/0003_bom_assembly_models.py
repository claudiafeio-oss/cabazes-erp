"""bom and assembly models

Revision ID: 0003_bom_assembly_models
Revises: 0002_purchase_models
Create Date: 2026-03-07 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0003_bom_assembly_models"
down_revision = "0002_purchase_models"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "substitution_groups",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
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
            nullable=False,
        ),
    )
    op.create_table(
        "substitution_group_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("substitution_group_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["substitution_group_id"], ["substitution_groups.id"]
        ),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
    )
    op.create_table(
        "basket_boms",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("basket_product_id", sa.Integer(), nullable=False),
        sa.Column("version", sa.String(length=32), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
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
        sa.ForeignKeyConstraint(["basket_product_id"], ["products.id"]),
    )
    op.create_table(
        "basket_bom_lines",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("basket_bom_id", sa.Integer(), nullable=False),
        sa.Column("component_product_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Numeric(14, 3), nullable=False),
        sa.Column("substitution_group_id", sa.Integer()),
        sa.ForeignKeyConstraint(["basket_bom_id"], ["basket_boms.id"]),
        sa.ForeignKeyConstraint(["component_product_id"], ["products.id"]),
        sa.ForeignKeyConstraint(
            ["substitution_group_id"], ["substitution_groups.id"]
        ),
    )
    op.create_table(
        "assembly_orders",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("basket_product_id", sa.Integer(), nullable=False),
        sa.Column("basket_bom_id", sa.Integer()),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("planned_quantity", sa.Numeric(14, 3), nullable=False),
        sa.Column("produced_quantity", sa.Numeric(14, 3), nullable=False),
        sa.Column("scheduled_at", sa.DateTime(timezone=True)),
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
        sa.ForeignKeyConstraint(["basket_product_id"], ["products.id"]),
        sa.ForeignKeyConstraint(["basket_bom_id"], ["basket_boms.id"]),
    )
    op.create_table(
        "assembly_order_planned_lines",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("assembly_order_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("quantity_planned", sa.Numeric(14, 3), nullable=False),
        sa.Column("substitution_group_id", sa.Integer()),
        sa.ForeignKeyConstraint(["assembly_order_id"], ["assembly_orders.id"]),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.ForeignKeyConstraint(
            ["substitution_group_id"], ["substitution_groups.id"]
        ),
    )
    op.create_table(
        "assembly_order_consumption_lines",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("assembly_order_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("lot_id", sa.Integer()),
        sa.Column("quantity_consumed", sa.Numeric(14, 3), nullable=False),
        sa.Column("planned_product_id", sa.Integer()),
        sa.Column("substitution_group_id", sa.Integer()),
        sa.ForeignKeyConstraint(["assembly_order_id"], ["assembly_orders.id"]),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.ForeignKeyConstraint(["lot_id"], ["lots.id"]),
        sa.ForeignKeyConstraint(["planned_product_id"], ["products.id"]),
        sa.ForeignKeyConstraint(
            ["substitution_group_id"], ["substitution_groups.id"]
        ),
    )
    op.create_table(
        "assembly_order_output_lines",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("assembly_order_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("lot_id", sa.Integer()),
        sa.Column("quantity_produced", sa.Numeric(14, 3), nullable=False),
        sa.Column("expiry_date", sa.Date()),
        sa.ForeignKeyConstraint(["assembly_order_id"], ["assembly_orders.id"]),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.ForeignKeyConstraint(["lot_id"], ["lots.id"]),
    )


def downgrade() -> None:
    op.drop_table("assembly_order_output_lines")
    op.drop_table("assembly_order_consumption_lines")
    op.drop_table("assembly_order_planned_lines")
    op.drop_table("assembly_orders")
    op.drop_table("basket_bom_lines")
    op.drop_table("basket_boms")
    op.drop_table("substitution_group_items")
    op.drop_table("substitution_groups")
