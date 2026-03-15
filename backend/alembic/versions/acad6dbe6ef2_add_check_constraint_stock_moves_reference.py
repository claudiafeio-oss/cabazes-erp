"""add_check_constraint_stock_moves_reference

Revision ID: acad6dbe6ef2
Revises: 0005_supplier_products
Create Date: 2026-03-15 17:02:12.462071
"""
from alembic import op

revision = 'acad6dbe6ef2'
down_revision = '0005_supplier_products'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_check_constraint(
        'ck_stock_moves_reference_consistency',
        'stock_moves',
        '(reference_type IS NULL) = (reference_id IS NULL)',
    )


def downgrade() -> None:
    op.drop_constraint(
        'ck_stock_moves_reference_consistency',
        'stock_moves',
        type_='check',
    )
