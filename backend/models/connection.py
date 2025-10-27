from enum import Enum as PyEnum
from sqlalchemy import String, BigInteger, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database import Base
from backend.models.mixins import ChangesMixin


class ConnectionStatus(str, PyEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DELISTED = "DELISTED"
    PENDING = "PENDING"
    ERROR = "ERROR"
    REVOKED = "REVOKED"


# === MODEL ===
class Connection(Base, ChangesMixin):
    __tablename__ = "connections"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(
        "users.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    broker_code: Mapped[str] = mapped_column(String(64), nullable=False)
    strategy: Mapped[str] = mapped_column(String(64), nullable=False)

    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[ConnectionStatus] = mapped_column(
        Enum(ConnectionStatus, name="connection_status"),
        nullable=False,
        server_default=ConnectionStatus.PENDING.value,
    )
    access_token: Mapped[str | None] = mapped_column(
        String(128), nullable=True)
    account_id: Mapped[str | None] = mapped_column(String(128), nullable=True)

    # relationships
    user: Mapped[list["User"]] = relationship(back_populates="connections")
    portfolio_connections = relationship(
        "PortfolioConnection",
        back_populates="connection",
    )
    portfolios = relationship(
        "Portfolio",
        secondary="portfolios_connections",
        back_populates="connections",
        viewonly=True,
    )
