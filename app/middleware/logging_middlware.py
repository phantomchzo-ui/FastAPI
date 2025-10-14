import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from app.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()

        logger.info({
            "event": "request",
            "method": request.method,
            "url": str(request.url),
            "client": request.client.host if request.client else None,
        })

        try:
            response: Response = await call_next(request)
        except Exception as e:
            logger.error({
                "event": "error",
                "error": str(e),
                "method": request.method,
                "url": str(request.url),
            })
            raise

        process_time = round(time.perf_counter() - start_time, 4)
        response.headers["X-Process-Time"] = str(process_time)

        logger.info({
            "event": "response",
            "status_code": response.status_code,
            "method": request.method,
            "url": str(request.url),
            "process_time": process_time
        })

        return response
