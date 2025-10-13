from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database import Base
from backend.models.mixins import ChangesMixin



class Portfolio(Base, ChangesMixin):
    __tablename__ = "portfolios"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    broker_type: Mapped[str | None] = mapped_column(String(50), nullable=True)  # "tinkoff","sber","alor",...

    user: Mapped["User"] = relationship(back_populates="portfolios")
    trades: Mapped[list["Trade"]] = relationship(back_populates="portfolio")
