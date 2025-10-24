from enum import Enum as PyEnum
from typing import Optional
from sqlalchemy import String, BigInteger, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database import Base
from backend.models.mixins import ChangesMixin


# === MODEL ===
class PortfolioConnection(Base, ChangesMixin):
    __tablename__ = "portfolios_connections"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    portfolio_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False)
    connection_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("connections.id", ondelete="CASCADE"), nullable=False)

    # relationships
    portfolio = relationship("Portfolio", back_populates="portfolio_connections")
    connection = relationship("Connection", back_populates="portfolio_connections")