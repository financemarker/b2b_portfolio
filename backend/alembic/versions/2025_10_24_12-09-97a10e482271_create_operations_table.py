"""create operations table

Revision ID: 97a10e482271
Revises: a48fe9a644c9
Create Date: 2025-10-24 12:09:53.500419

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97a10e482271'
down_revision: Union[str, Sequence[str], None] = 'a48fe9a644c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "operations",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("portfolio_id", sa.BigInteger, sa.ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False),
        sa.Column("instrument_id", sa.BigInteger, sa.ForeignKey("instruments.id", ondelete="CASCADE"), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source", sa.String(length=64), nullable=True),

      
        sa.Column('created_by', sa.String(length=64), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.Column('changed_by', sa.String(length=64), nullable=True),
        sa.Column('changed_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
    )

    # Индексы/Уникальности
    op.create_index("ix_operations_portfolio", "operations", ["portfolio_id"])
    op.create_index("ix_operations_instrument", "operations", ["instrument_id"])


def downgrade():
    op.drop_index("ix_operations_instrument", table_name="connections")
    op.drop_index("ix_operations_portfolio", table_name="connections")
    op.drop_table("operations")
