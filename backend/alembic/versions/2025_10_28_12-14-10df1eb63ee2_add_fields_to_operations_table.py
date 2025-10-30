"""add_fields_to_operations_table

Revision ID: 10df1eb63ee2
Revises: cbab859fa519
Create Date: 2025-10-28 12:14:15.982482

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10df1eb63ee2'
down_revision: Union[str, Sequence[str], None] = 'cbab859fa519'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add new columns to operations table
    op.add_column('operations', sa.Column('broker_operation_id', sa.String(length=128), nullable=True))
    op.add_column('operations', sa.Column('operation_type', sa.String(length=32), nullable=False))

    # Quantity and price
    op.add_column('operations', sa.Column('quantity', sa.Numeric(precision=20, scale=8), nullable=True))
    op.add_column('operations', sa.Column('price', sa.Numeric(precision=20, scale=8), nullable=True))
    op.add_column('operations', sa.Column('price_currency', sa.String(length=3), nullable=True))

    # Commission
    op.add_column('operations', sa.Column('commission', sa.Numeric(precision=20, scale=8), nullable=True))
    op.add_column('operations', sa.Column('commission_currency', sa.String(length=3), nullable=True))

    # Tax
    op.add_column('operations', sa.Column('tax', sa.Numeric(precision=20, scale=8), nullable=True))
    op.add_column('operations', sa.Column('tax_currency', sa.String(length=3), nullable=True))

    # Accrued interest (for bonds)
    op.add_column('operations', sa.Column('accrued_interest', sa.Numeric(precision=20, scale=8), nullable=True))
    op.add_column('operations', sa.Column('accrued_interest_currency', sa.String(length=3), nullable=True))

    # Payment (main financial field)
    op.add_column('operations', sa.Column('payment', sa.Numeric(precision=20, scale=8), nullable=False))
    op.add_column('operations', sa.Column('payment_currency', sa.String(length=3), nullable=False))
    
    # Additional info
    op.add_column('operations', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('operations', sa.Column('raw_data', sa.JSON(), nullable=True))

    # Create indexes
    # Unique index for broker operations (only where broker_operation_id is not null)
    op.create_index(
        'ix_operations_broker_id_portfolio',
        'operations',
        ['broker_operation_id', 'portfolio_id'],
        unique=True
    )

    # Index for portfolio operations sorted by timestamp
    op.create_index('ix_operations_portfolio_timestamp', 'operations', ['portfolio_id', sa.text('timestamp DESC')])

    # Index for instrument operations sorted by timestamp
    op.create_index(
        'ix_operations_instrument_timestamp',
        'operations',
        ['instrument_id', sa.text('timestamp DESC')],
        postgresql_where=sa.text('instrument_id IS NOT NULL')
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop indexes
    op.drop_index('ix_operations_instrument_timestamp', table_name='operations')
    op.drop_index('ix_operations_portfolio_timestamp', table_name='operations')
    op.drop_index('ix_operations_broker_id_portfolio', table_name='operations')

    # Drop columns
    op.drop_column('operations', 'raw_data')
    op.drop_column('operations', 'description')
    op.drop_column('operations', 'accrued_interest_currency')
    op.drop_column('operations', 'accrued_interest')
    op.drop_column('operations', 'tax_currency')
    op.drop_column('operations', 'tax')
    op.drop_column('operations', 'commission_currency')
    op.drop_column('operations', 'commission')
    op.drop_column('operations', 'payment_currency')
    op.drop_column('operations', 'payment')
    op.drop_column('operations', 'price_currency')
    op.drop_column('operations', 'price')
    op.drop_column('operations', 'quantity')
    op.drop_column('operations', 'operation_type')
    op.drop_column('operations', 'broker_operation_id')
