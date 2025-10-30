from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy import String, BigInteger, ForeignKey, DateTime, Numeric, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database import Base
from backend.models.mixins import ChangesMixin


# === MODEL ===
class Operation(Base, ChangesMixin):
    __tablename__ = "operations"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    portfolio_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("portfolios.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    instrument_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("instruments.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    source: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)

    # Broker identification
    broker_operation_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)

    # Operation type and state
    operation_type: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)

    # Quantity and price
    quantity: Mapped[Optional[Decimal]] = mapped_column(Numeric(20, 8), nullable=True)
    price: Mapped[Optional[Decimal]] = mapped_column(Numeric(20, 8), nullable=True)
    price_currency: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)

    # Commission
    commission: Mapped[Optional[Decimal]] = mapped_column(Numeric(20, 8), nullable=True)
    commission_currency: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)

    # Tax
    tax: Mapped[Optional[Decimal]] = mapped_column(Numeric(20, 8), nullable=True)
    tax_currency: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)

    # Accrued interest (for bonds)
    accrued_interest: Mapped[Optional[Decimal]] = mapped_column(Numeric(20, 8), nullable=True)
    accrued_interest_currency: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)

    # Payment (main financial field)
    payment: Mapped[Optional[Decimal]] = mapped_column(Numeric(20, 8), nullable=True)
    payment_currency: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)

    # Additional info
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    raw_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # relationships
    instrument: Mapped["Instrument"] = relationship(back_populates="operations")
    portfolio: Mapped["Portfolio"] = relationship(back_populates="operations")
