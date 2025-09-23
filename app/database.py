from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)

async_session = async_sessionmaker(engine)

class Base(DeclarativeBase):
    pass

async def get_session():
    async with async_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]