"""create portfolios_connections table

Revision ID: cbab859fa519
Revises: 97a10e482271
Create Date: 2025-10-24 12:24:04.328673

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cbab859fa519'
down_revision: Union[str, Sequence[str], None] = '97a10e482271'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "portfolios_connections",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("portfolio_id", sa.BigInteger, sa.ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False),
        sa.Column("connection_id", sa.BigInteger, sa.ForeignKey("connections.id", ondelete="CASCADE"), nullable=False),


        sa.Column('created_by', sa.String(length=64), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.Column('changed_by', sa.String(length=64), nullable=True),
        sa.Column('changed_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
    )

    op.create_unique_constraint(
        "uq_portfolios_connections_pair",
        "portfolios_connections",
        ["portfolio_id", "connection_id"],
    )
    op.create_index("ix_portfolios_connections_portfolio", "portfolios_connections", ["portfolio_id"])
    op.create_index("ix_portfolios_connections_connection", "portfolios_connections", ["connection_id"])


def downgrade():
    op.drop_index("ix_portfolios_connections_connection", table_name="portfolios_connections")
    op.drop_index("ix_portfolios_connections_portfolio", table_name="portfolios_connections")
    op.drop_constraint("uq_portfolios_connections_pair", "portfolios_connections", type_="unique")
    op.drop_table("portfolios_connections")