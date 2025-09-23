from pydantic import EmailStr
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, engine


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    email: Mapped[EmailStr] = mapped_column(String(50))
    hashed_password: Mapped[str]
    role: Mapped[str] = mapped_column(String(25), default='user')

