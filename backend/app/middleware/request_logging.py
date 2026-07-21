"""Structured request/response logging middleware."""

import time
import uuid
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())[:8]
        start = time.perf_counter()

        response = await call_next(request)

        elapsed = time.perf_counter() - start
        logger.info(
            "%s  %s %s  %s  %.0fms",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            elapsed * 1000,
        )
        return response
