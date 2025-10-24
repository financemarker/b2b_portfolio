from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.core.database import Base
from backend.models.mixins import ChangesMixin


class Portfolio(Base, ChangesMixin):
    __tablename__ = "portfolios"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(
        "users.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    # "tinkoff","sber","alor",...
    broker_code: Mapped[str] = mapped_column(String(50), nullable=False)

    user: Mapped["User"] = relationship(back_populates="portfolios")
    operations: Mapped[list["Operation"]] = relationship(
        back_populates="portfolio")

    portfolio_connections = relationship(
        "PortfolioConnection",
        back_populates="portfolio",
    )
    # Дополнительно, «удобная» viewonly-связь напрямую на Connection:
    connections = relationship(
        "Connection",
        secondary="portfolios_connections",
        viewonly=True,
    )
