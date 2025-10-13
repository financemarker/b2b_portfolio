from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database import Base
from backend.models.mixins import ChangesMixin

class Role(Base, ChangesMixin):
    __tablename__ = "roles"

    code: Mapped[str] = mapped_column(String(32), primary_key=True)  # "admin","pro","demo"
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    clients: Mapped[list["Client"]] = relationship(back_populates="role")
