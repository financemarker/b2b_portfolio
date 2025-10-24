from backend.models.mixins import ChangesMixin
from backend.models.role import Role
from backend.models.client import Client
from backend.models.user import User
from backend.models.portfolio import Portfolio
from backend.models.order import Order
from backend.models.exchange import Exchange
from backend.models.instrument import Instrument
from backend.models.portfolio_connection import PortfolioConnection
from backend.models.connection import Connection
from backend.models.operation import Operation

# экспортируем metadata, чтобы Alembic и база знали, что использовать
from backend.core.database import Base

metadata = Base.metadata

__all__ = [
    "ChangesMixin",
    "Role",
    "Client",
    "User",
    "Portfolio",
    "Order",
    "Exchange",
    "Instrument",
    "PortfolioConnection",
    "Connection",
    "Operation",
    "metadata",
]
