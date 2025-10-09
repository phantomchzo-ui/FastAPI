import re

from pydantic import EmailStr
from sqlalchemy import select, insert, delete, update

from app.database import async_session


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id):
        async with async_session() as session:
            query = select(cls.model).filter_by(id=model_id)
            res = await session.execute(query)
            return res.scalar_one_or_none()

    @classmethod
    async def find_one_ore_none(cls, **filter_by):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            res = await session.execute(query)
            return res.scalar_one_or_none()

    @classmethod
    async def find_all(cls):
        async with async_session() as session:
            query = select(cls.model)
            res = await session.execute(query)
            return res.scalars().all()

    @classmethod
    async def add(cls, **data):
        async with async_session() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def remove(cls, model_id:int):
        async with async_session() as session:
            query = delete(cls.model).where(cls.model.id==model_id)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update(cls, model_id: int, data: dict):
        async with async_session() as session:
            query = (update(cls.model).where(cls.model.id==model_id).values(**data).returning(cls.model))
            await session.execute(query)
            await session.commit()

    @classmethod
    async def patch(cls, email: EmailStr, new_password: str):
        async with async_session() as session:
            query = (update(cls.model).where(cls.model.email==email).values(hashed_password=new_password).
                     returning(cls.model))
            await session.execute(query)
            await session.commit()


def validation_password(password:str) -> str:
        if len(password) < 6:
            raise ValueError('Пароль должен содержать минимум 6 символов')
        if not re.search(r"[A-Z]", password):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву')
        if not re.search(r"[a-z]", password):
            raise ValueError("Пароль должен содержать хотя бы одну строчную букву")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError("Пароль должен содержать хотя бы один спецсимвол")
        return password

