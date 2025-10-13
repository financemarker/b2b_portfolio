from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database import Base
from backend.models.mixins import ChangesMixin


class Trade(Base, ChangesMixin):
    __tablename__ = "trades"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolios.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

    portfolio: Mapped["Portfolio"] = relationship(back_populates="trades")
