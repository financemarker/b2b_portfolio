"""update_operations_unique_constraint

Revision ID: df2c13f65a4c
Revises: 10df1eb63ee2
Create Date: 2025-11-21 15:13:53.842837

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df2c13f65a4c'
down_revision: Union[str, Sequence[str], None] = '10df1eb63ee2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_index('ix_operations_broker_id_portfolio', table_name='operations')

    op.create_unique_constraint(
        'uq_operations_portfolio_source_broker_id',
        'operations',
        ['portfolio_id', 'source', 'broker_operation_id']
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('uq_operations_portfolio_source_broker_id', 'operations', type_='unique')

    op.create_index(
        'ix_operations_broker_id_portfolio',
        'operations',
        ['broker_operation_id', 'portfolio_id'],
        unique=True
    )
