from sqlalchemy import select

from app.catalog.model import Catalog
from app.dao.base import BaseDAO
from app.database import async_session
from app.products.model import Product


class ProductDAO(BaseDAO):
    model = Product

    @classmethod
    async def find_by_category(cls, catalog_id: int):
        async with async_session() as session:
            query = select(cls.model).where(cls.model.catalog_id == catalog_id)
            res = await session.execute(query)
            return res.scalars().all()

    @classmethod
    async def product_find_all(cls, limit: int = 10, offset: int = 0):
        async with async_session() as session:
            query = select(cls.model).limit(limit).offset(offset)
            res = await session.execute(query)
            return res.scalars().all()

