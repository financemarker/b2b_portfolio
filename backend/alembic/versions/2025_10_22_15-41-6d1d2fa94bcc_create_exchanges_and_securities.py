"""create exchanges and securities

Revision ID: 6d1d2fa94bcc
Revises: 042a705cf34d
Create Date: 2025-10-22 15:41:07.852256

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d1d2fa94bcc'
down_revision: Union[str, Sequence[str], None] = '042a705cf34d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "exchanges",
        sa.Column("code", sa.String(length=10),
                  primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("country", sa.String(length=3), nullable=False),
        sa.Column("currency", sa.String(3), nullable=True),
        sa.Column('created_by', sa.String(length=64), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('changed_by', sa.String(length=64), nullable=True),
        sa.Column('changed_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    op.create_table(
        "instruments",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("exchange_code", sa.String(10), sa.ForeignKey(
            "exchanges.code", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False),
        sa.Column("code", sa.String(30), nullable=False),
        sa.Column("isin", sa.String(12), nullable=True),
        sa.Column("figi", sa.String(20), nullable=True),
        sa.Column("cusip", sa.String(9), nullable=True),
        sa.Column("sedol", sa.String(10), nullable=True),
        sa.Column("name", sa.String(255), nullable=True),
        sa.Column(
            "category",
            sa.Enum(
                "stock", "bond", "fund", "commodity", "currency", "crypto", "other",
                name="instrument_category",
            ),
            nullable=False,
        ),
        sa.Column("currency", sa.String(3), nullable=True),
        sa.Column(
            "status",
            sa.Enum("active", "inactive", "delisted",
                    name="instrument_status"),
            nullable=False,
            server_default="active",
        ),
        sa.Column('created_by', sa.String(length=64), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('changed_by', sa.String(length=64), nullable=True),
        sa.Column('changed_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    op.create_index("ix_instruments_exchange_code", "instruments", ["exchange_code", "code"])
    op.create_index("ix_instruments_isin", "instruments", ["isin"])
    op.create_index("ix_instruments_figi", "instruments", ["figi"])


def downgrade() -> None:
    op.drop_index("ix_instruments_exchange_code", table_name="instruments")
    op.drop_index("ix_instruments_figi", table_name="instruments")
    op.drop_index("ix_instruments_isin", table_name="instruments")

    op.drop_table("instruments")
    op.drop_table("exchanges")

    sa.Enum(name="instrument_category").drop(op.get_bind())
    sa.Enum(name="instrument_status").drop(op.get_bind())
