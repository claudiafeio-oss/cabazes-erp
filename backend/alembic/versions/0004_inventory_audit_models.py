"""inventory and audit models

Revision ID: 0004_inventory_audit_models
Revises: 0003_bom_assembly_models
Create Date: 2026-03-07 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0004_inventory_audit_models"
down_revision = "0003_bom_assembly_models"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "inventory_adjustments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("location_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("counted_at", sa.DateTime(timezone=True)),
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
        sa.ForeignKeyConstraint(["location_id"], ["locations.id"]),
    )
    op.create_table(
        "inventory_adjustment_lines",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("adjustment_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("lot_id", sa.Integer()),
        sa.Column("quantity_counted", sa.Numeric(14, 3), nullable=False),
        sa.Column("quantity_system", sa.Numeric(14, 3), nullable=False),
        sa.Column("quantity_difference", sa.Numeric(14, 3), nullable=False),
        sa.ForeignKeyConstraint(["adjustment_id"], ["inventory_adjustments.id"]),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.ForeignKeyConstraint(["lot_id"], ["lots.id"]),
    )
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("actor_user_id", sa.Integer()),
        sa.Column("action", sa.String(length=64), nullable=False),
        sa.Column("entity_type", sa.String(length=64), nullable=False),
        sa.Column("entity_id", sa.Integer()),
        sa.Column("payload", sa.JSON()),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["actor_user_id"], ["users.id"]),
    )


def downgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_table("inventory_adjustment_lines")
    op.drop_table("inventory_adjustments")
