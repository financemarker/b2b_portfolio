from enum import Enum as PyEnum
from typing import Optional
from sqlalchemy import String, BigInteger, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database import Base
from backend.models.mixins import ChangesMixin


# === ENUM TYPES ===
class InstrumentCategory(str, PyEnum):
    STOCK = "STOCK"
    BOND = "BOND"
    FUND = "FUND"
    COMMODITY = "COMMODITY"
    CURRENCY = "CURRENCY"
    CRYPTO = "CRYPTO"
    OTHER = "OTHER"


class InstrumentStatus(str, PyEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DELISTED = "DELISTED"


# === MODEL ===
class Instrument(Base, ChangesMixin):
    __tablename__ = "instruments"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    # Foreign key
    exchange_code: Mapped[str] = mapped_column(
        String(10),
        ForeignKey("exchanges.code", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )

    code: Mapped[str] = mapped_column(String(30), nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(255))

    isin: Mapped[Optional[str]] = mapped_column(String(12))
    cusip: Mapped[Optional[str]] = mapped_column(String(9))
    figi: Mapped[Optional[str]] = mapped_column(String(20))
    sedol: Mapped[Optional[str]] = mapped_column(String(10))

    category: Mapped[InstrumentCategory] = mapped_column(
        Enum(InstrumentCategory, name="instrument_category"), nullable=False
    )

    currency: Mapped[Optional[str]] = mapped_column(String(3))
    status: Mapped[InstrumentStatus] = mapped_column(
        Enum(InstrumentStatus, name="instrument_status"),
        nullable=False,
        server_default=InstrumentStatus.ACTIVE.value,
    )

    # ORM relationships
    exchange: Mapped["Exchange"] = relationship(back_populates="instruments")
    operations: Mapped[list["Operation"]] = relationship(back_populates="instrument")