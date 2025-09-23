from fastapi import FastAPI
from sqladmin import Admin
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.admin.admin import UserAdmin, ProductAdmin, CatalogAdmin
from app.admin.auth import authentication_backend
from app.database import engine
from app.users.router import router
from app.catalog.router import router as catalog_router
from app.products.router import router as product_router

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend


from redis import asyncio as aioredis

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(ProductAdmin)
admin.add_view(CatalogAdmin)

app.include_router(router)
app.include_router(catalog_router)
app.include_router(product_router)

