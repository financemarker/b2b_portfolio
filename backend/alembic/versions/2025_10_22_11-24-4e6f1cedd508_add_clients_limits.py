"""add clients limits

Revision ID: 4e6f1cedd508
Revises: c13993c96da9
Create Date: 2025-10-22 11:24:07.330180

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e6f1cedd508'
down_revision: Union[str, Sequence[str], None] = 'c13993c96da9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # === clients ===
    op.add_column("clients", sa.Column("users_limit", sa.Integer(), nullable=True))
    op.add_column("clients", sa.Column("users_count", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("clients", sa.Column("user_portfolios_limit", sa.Integer(), nullable=True))
    op.add_column("clients", sa.Column("api_requests_limit", sa.Integer(), nullable=True))
    op.add_column("clients", sa.Column("api_requests_remaining", sa.Integer(), nullable=True))

    # === users ===
    op.add_column("users", sa.Column("portfolios_count", sa.Integer(), nullable=False, server_default="0"))


def downgrade() -> None:
    # === users ===
    op.drop_column("users", "portfolios_count")

    # === clients ===
    op.drop_column("clients", "api_requests_remaining")
    op.drop_column("clients", "api_requests_limit")
    op.drop_column("clients", "user_portfolios_limit")
    op.drop_column("clients", "users_count")
    op.drop_column("clients", "users_limit")
