"""create connections table

Revision ID: a48fe9a644c9
Revises: 6d1d2fa94bcc
Create Date: 2025-10-23 17:16:42.167465

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a48fe9a644c9'
down_revision: Union[str, Sequence[str], None] = '6d1d2fa94bcc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "connections",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("user_id", sa.BigInteger, sa.ForeignKey(
            "users.id", ondelete="CASCADE"), nullable=False),

        # tinkoff / finam / ibkr ...
        sa.Column("broker_code", sa.String(length=64), nullable=False),
        # token / api / file / oauth2 ...
        sa.Column("strategy", sa.String(length=64), nullable=False),

        # произвольное имя соединения
        sa.Column("name", sa.String(length=255), nullable=True),
        sa.Column(
            "status",
            sa.Enum('active', 'pending', 'inactive', 'error', 'revoked',
                    name="connection_status"),
            nullable=False,
            server_default="pending",
        ),

        # Храним технические детали подключения. Рекомендация: шифровать секретные поля на уровне приложения.
        sa.Column("access_token", sa.String(length=128), nullable=True),
        # Внешние идентификаторы со стороны интеграции (если нужны)
        sa.Column("account_id", sa.String(length=128), nullable=True),

        sa.Column('created_by', sa.String(length=64), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.Column('changed_by', sa.String(length=64), nullable=True),
        sa.Column('changed_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
    )

    # Индексы/Уникальности
    op.create_index("ix_connections_user", "connections", ["user_id"])
    op.create_index("ix_connections_user_broker",
                    "connections", ["user_id", "broker_code"])
    # Разрешаем несколько соединений одного брокера, но:
    # если external_connection_id есть, то делаем уникальность в разрезе user+broker+external_connection_id
    op.create_unique_constraint(
        "uq_connections_user_broker_account",
        "connections",
        ["user_id", "broker_code", "account_id"],
    )


def downgrade():
    op.drop_constraint("uq_connections_user_broker_account",
                       "connections", type_="unique")
    op.drop_index("ix_connections_user_broker", table_name="connections")
    op.drop_index("ix_connections_user", table_name="connections")
    op.drop_table("connections")
