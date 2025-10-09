from sqlalchemy import Column, BigInteger, String, DateTime, text
from datetime import datetime
from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)

    # кто создал и кто изменил
    created_by = Column(String, nullable=True)
    changed_by = Column(String, nullable=True)

    # даты создания / изменения
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),  # на уровне БД
        default=datetime.now,                   # на уровне Python
    )

    changed_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        default=datetime.now,
        onupdate=datetime.now,                  # Python при update
        # server_onupdate=text("CURRENT_TIMESTAMP"), # не актуально для postgress
    )
