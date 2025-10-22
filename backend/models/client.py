from sqlalchemy import BigInteger, String, ForeignKey, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from backend.core.database import Base
from backend.models.mixins import ChangesMixin


class Client(Base, ChangesMixin):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role_code: Mapped[str] = mapped_column(ForeignKey("roles.code", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    api_token: Mapped[str | None] = mapped_column(String(128), nullable=True, unique=True)
    valid_to: Mapped[date | None] = mapped_column(Date, nullable=True)

    # --- лимиты и счетчики ---
    users_limit: Mapped[int | None] = mapped_column(nullable=True)
    users_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    user_portfolios_limit: Mapped[int | None] = mapped_column(nullable=True)
    api_requests_limit: Mapped[int | None] = mapped_column(nullable=True)
    api_requests_remaining: Mapped[int | None] = mapped_column(nullable=True)

    # relations
    role: Mapped["Role"] = relationship(back_populates="clients")
    users: Mapped[list["User"]] = relationship(back_populates="client")
    orders: Mapped[list["Order"]] = relationship(back_populates="client")

    @property
    def is_admin(self) -> bool:
        return (self.role and self.role.level >= 9)