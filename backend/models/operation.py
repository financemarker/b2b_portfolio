from datetime import datetime
from sqlalchemy import String, BigInteger, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database import Base
from backend.models.mixins import ChangesMixin


# === MODEL ===
class Operation(Base, ChangesMixin):
    __tablename__ = "operations"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    portfolio_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("portfolios.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    instrument_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("instruments.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False )
    source: Mapped[str] = mapped_column(String(64), nullable=True)

    # relationships
    instrument: Mapped["Instrument"] = relationship(back_populates="operations")
    portfolio: Mapped["Portfolio"] = relationship(back_populates="operations")
