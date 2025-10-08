from typing import Annotated

from fastapi import Depends
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


if settings.MODE == "TEST":
    database_url = settings.test_database_url
    database_param ={"poolclass": NullPool}
else:
    database_url = settings.database_url
    database_param = {}

engine = create_async_engine(database_url, **database_param)

async_session = async_sessionmaker(engine)

class Base(DeclarativeBase):
    pass

async def get_session():
    async with async_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]