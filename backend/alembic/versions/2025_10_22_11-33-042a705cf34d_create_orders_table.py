"""create orders table

Revision ID: 042a705cf34d
Revises: 4e6f1cedd508
Create Date: 2025-10-22 11:33:04.668435

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '042a705cf34d'
down_revision: Union[str, Sequence[str], None] = '4e6f1cedd508'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table("orders",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("invoice_id", sa.String(length=50), nullable=False, unique=True),
        sa.Column("client_id", sa.Integer(), sa.ForeignKey( "clients.id", onupdate='CASCADE', ondelete='RESTRICT'), nullable=False),
        sa.Column("item", sa.String(length=100), nullable=False),
        sa.Column("price", sa.Numeric(12, 2), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="pending"),
        sa.Column("promocode", sa.String(length=50), nullable=True),
        sa.Column('created_by', sa.String(length=64), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('changed_by', sa.String(length=64), nullable=True),
        sa.Column('changed_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    op.create_index("ix_orders_client_id", "orders", ["client_id"])


def downgrade():
    op.drop_index("ix_orders_client_id", table_name="orders")
    op.drop_table("orders")
