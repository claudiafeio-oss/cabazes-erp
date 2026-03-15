"""core models

Revision ID: 0001_core_models
Revises: None
Create Date: 2026-03-07 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0001_core_models"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255)),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
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
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("sku", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("product_type", sa.String(length=32), nullable=False),
        sa.Column("unit_of_measure", sa.String(length=32), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("track_lot", sa.Boolean(), nullable=False),
        sa.Column("track_expiry", sa.Boolean(), nullable=False),
        sa.Column("minimum_stock", sa.Numeric(14, 3), nullable=False),
        sa.Column("default_cost", sa.Numeric(14, 4), nullable=False),
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
        sa.UniqueConstraint("sku"),
    )
    op.create_table(
        "suppliers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(length=64), nullable=False),
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
        sa.UniqueConstraint("code"),
    )
    op.create_table(
        "locations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(length=64), nullable=False),
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
        sa.UniqueConstraint("code"),
    )
    op.create_table(
        "lots",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("lot_code", sa.String(length=64), nullable=False),
        sa.Column("expiry_date", sa.Date()),
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
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.UniqueConstraint("product_id", "lot_code"),
    )
    op.create_table(
        "stock_moves",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("location_id", sa.Integer(), nullable=False),
        sa.Column("lot_id", sa.Integer()),
        sa.Column("quantity", sa.Numeric(14, 3), nullable=False),
        sa.Column("move_type", sa.String(length=32), nullable=False),
        sa.Column("reference_type", sa.String(length=32)),
        sa.Column("reference_id", sa.Integer()),
        sa.Column("unit_cost", sa.Numeric(14, 4)),
        sa.Column(
            "occurred_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.ForeignKeyConstraint(["location_id"], ["locations.id"]),
        sa.ForeignKeyConstraint(["lot_id"], ["lots.id"]),
    )
    op.create_index(
        "ix_stock_moves_product_location",
        "stock_moves",
        ["product_id", "location_id"],
    )
    op.create_index("ix_stock_moves_lot", "stock_moves", ["lot_id"])
    op.create_index("ix_stock_moves_occurred_at", "stock_moves", ["occurred_at"])
    op.create_table(
        "stock_balance",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("location_id", sa.Integer(), nullable=False),
        sa.Column("lot_id", sa.Integer()),
        sa.Column("quantity", sa.Numeric(14, 3), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.ForeignKeyConstraint(["location_id"], ["locations.id"]),
        sa.ForeignKeyConstraint(["lot_id"], ["lots.id"]),
        sa.UniqueConstraint("product_id", "location_id", "lot_id"),
    )


def downgrade() -> None:
    op.drop_table("stock_balance")
    op.drop_index("ix_stock_moves_occurred_at", table_name="stock_moves")
    op.drop_index("ix_stock_moves_lot", table_name="stock_moves")
    op.drop_index("ix_stock_moves_product_location", table_name="stock_moves")
    op.drop_table("stock_moves")
    op.drop_table("lots")
    op.drop_table("locations")
    op.drop_table("suppliers")
    op.drop_table("products")
    op.drop_table("users")
