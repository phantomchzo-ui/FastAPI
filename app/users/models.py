from datetime import datetime

from pydantic import EmailStr
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime
from app.database import Base, engine


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    email: Mapped[EmailStr] = mapped_column(String(50))
    hashed_password: Mapped[str]
    balance:Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    role: Mapped[str] = mapped_column(String(25), default='user')


