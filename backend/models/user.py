from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.core.database import Base
from backend.models.mixins import ChangesMixin

class User(Base, ChangesMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    external_id: Mapped[str] = mapped_column(String(128), nullable=False)

    client: Mapped["Client"] = relationship(back_populates="users")
    portfolios: Mapped[list["Portfolio"]] = relationship(back_populates="user")