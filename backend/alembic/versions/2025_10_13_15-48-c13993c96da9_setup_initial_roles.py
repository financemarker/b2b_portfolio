"""setup initial roles

Revision ID: c13993c96da9
Revises: 0296fbe76ac8
Create Date: 2025-10-13 15:48:22.765539

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c13993c96da9'
down_revision: Union[str, Sequence[str], None] = '0296fbe76ac8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO roles (code, name, level)
        VALUES
          ('super_admin','Администратор',10),
          ('pro_user','Платный клиент',5),
          ('free_user','Зарегистрированный пользователь ',1)
        ON CONFLICT (code) DO NOTHING;
        """
    )



def downgrade() -> None:
    op.execute("DELETE FROM roles WHERE code IN ('super_admin','pro_user','free_user');")

