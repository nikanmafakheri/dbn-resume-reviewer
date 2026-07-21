"""Redis-backed sliding-window rate limiter middleware."""

import time
from collections.abc import Callable

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, redis_client, max_requests: int = 60, window_seconds: int = 60):
        super().__init__(app)
        self.redis = redis_client
        self.max_requests = max_requests
        self.window = window_seconds

    async def dispatch(self, request: Request, call_next):
        # Skip rate-limiting for non-user endpoints
        if request.url.path in ("/health", "/ready", "/metrics"):
            return await call_next(request)

        # TODO: implement sliding-window counter using Redis
        # key = f"rate_limit:{request.client.host}:{request.url.path}"
        # current = await self.redis.incr(key)
        # if current == 1:
        #     await self.redis.expire(key, self.window)

        return await call_next(request)
