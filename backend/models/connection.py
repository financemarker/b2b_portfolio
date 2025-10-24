from enum import Enum as PyEnum
from typing import Optional
from sqlalchemy import String, BigInteger, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database import Base
from backend.models.mixins import ChangesMixin


class ConnectionStatusEnum(str, PyEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELISTED = "delisted"
    PENDING = "pending"
    ERROR = "error"
    REVOKED = "revoked"


# === MODEL ===
class Connection(Base, ChangesMixin):
    __tablename__ = "connections"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(
        "users.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    broker_code: Mapped[str] = mapped_column(String(64), nullable=False)
    strategy: Mapped[str] = mapped_column(String(64), nullable=False)

    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(
        ConnectionStatusEnum, nullable=False, server_default="pending")

    access_token: Mapped[str | None] = mapped_column(
        String(128), nullable=True)
    account_id: Mapped[str | None] = mapped_column(String(128), nullable=True)

    # relationships
    user: Mapped[list["User"]] = relationship(back_populates="connections")
