import asyncio
import pytest

from app.config import settings
from app.database import Base, engine, async_session

from app.users.models import User
from app.catalog.model import Catalog
from app.products.model import Product

from app.main import app as fastapi_app
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    assert settings.MODE == "TEST", "Запуск тестов возможен только в режиме TEST!"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


    yield
    #async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def ac():
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac