from decimal import Decimal
from sqlalchemy import BigInteger, ForeignKey, String, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.core.database import Base
from backend.models.mixins import ChangesMixin

class Order(Base, ChangesMixin):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    invoice_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    item: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default="pending")
    promocode: Mapped[str | None] = mapped_column(String(50), nullable=True)


    client: Mapped["Client"] = relationship(back_populates="orders")