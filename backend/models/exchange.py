from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.core.database import Base
from backend.models.mixins import ChangesMixin


class Exchange(Base, ChangesMixin):
    __tablename__ = "exchanges"

    code: Mapped[str] = mapped_column(String(10), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(3), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)

    instruments: Mapped[list["Instrument"]] = relationship(back_populates="exchange")
