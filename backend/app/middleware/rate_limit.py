"""Redis-backed sliding-window rate limiter middleware."""

import logging
import time
from collections.abc import Awaitable, Callable

from fastapi import HTTPException, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

RequestResponseEndpoint = Callable[[Request], Awaitable[Response]]


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Sliding-window rate limiter using Redis.

    Falls back to a simple in-memory counter if Redis is unavailable,
    so the API never blocks on Redis failures.
    """

    def __init__(
        self,
        app,
        redis_client=None,
        max_requests: int = 60,
        window_seconds: int = 60,
    ):
        super().__init__(app)
        self.redis = redis_client
        self.max_requests = max_requests
        self.window = window_seconds
        # In-memory fallback
        self._memory_store: dict[str, list[float]] = {}

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Skip rate-limiting for health / docs
        if request.url.path in (
            "/health", "/ready", "/metrics", "/docs", "/redoc", "/openapi.json"
        ):
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        key = f"rate_limit:{client_ip}:{request.url.path}"

        if self.redis is not None:
            await self._check_redis(key)
        else:
            self._check_memory(key)

        return await call_next(request)

    async def _check_redis(self, key: str) -> None:
        """Sliding-window counter using Redis sorted sets."""
        import redis.asyncio as aioredis  # type: ignore[import-untyped]

        if not isinstance(self.redis, aioredis.Redis):
            self._check_memory(key)
            return

        now = time.time()
        window_start = now - self.window

        try:
            pipe = self.redis.pipeline()
            pipe.zremrangebyscore(key, 0, window_start)
            pipe.zcard(key)
            pipe.zadd(key, {str(now): now})
            pipe.expire(key, self.window)
            _, count, *_ = await pipe.execute()

            if count >= self.max_requests:
                raise HTTPException(status_code=429, detail="Too many requests")
        except HTTPException:
            raise
        except Exception as exc:
            logger.warning("Redis rate-limit check failed, falling back: %s", exc)
            self._check_memory(key)

    def _check_memory(self, key: str) -> None:
        """In-memory sliding-window fallback."""
        now = time.time()
        window_start = now - self.window

        timestamps = self._memory_store.get(key, [])
        timestamps = [t for t in timestamps if t > window_start]
        timestamps.append(now)
        self._memory_store[key] = timestamps

        if len(timestamps) > self.max_requests:
            raise HTTPException(status_code=429, detail="Too many requests")
