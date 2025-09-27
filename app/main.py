import time

from fastapi import FastAPI, Request
from sqladmin import Admin
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.admin.admin import UserAdmin, ProductAdmin, CatalogAdmin
from app.admin.auth import authentication_backend
from app.database import engine
from app.users.router import router
from app.users.router import public_router as public_router
from app.catalog.router import router as catalog_router
from app.products.router import router as product_router


from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from app.logger import logger

from redis import asyncio as aioredis

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield

app = FastAPI(lifespan=lifespan)

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(ProductAdmin)
admin.add_view(CatalogAdmin)

app.include_router(router)
app.include_router(public_router)
app.include_router(catalog_router)
app.include_router(product_router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.info(
        "HTTP Request",
        extra={
            "method": request.method,
            "url": str(request.url),
            "status_code": response.status_code,
            "process_time": round(process_time, 4)
        }
    )

    response.headers["X-Process-Time"] = str(round(process_time, 4))
    return response


