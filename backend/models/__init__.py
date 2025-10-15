from backend.models.mixins import ChangesMixin
from backend.models.role import Role
from backend.models.client import Client
from backend.models.user import User
from backend.models.portfolio import Portfolio
from backend.models.trade import Trade

# экспортируем metadata, чтобы Alembic и база знали, что использовать
from backend.core.database import Base

metadata = Base.metadata

__all__ = [
    "ChangesMixin",
    "Role",
    "Client",
    "User",
    "Portfolio",
    "Trade",
    "metadata",
]
