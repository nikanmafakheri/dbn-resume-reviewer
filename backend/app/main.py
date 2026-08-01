"""FastAPI application factory."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI  # type: ignore[import-not-found]

from app.core.config import settings
from app.core.database import close_db, init_database, init_db
from app.core.exceptions import AppException, app_exception_handler
from app.core.logging import configure_logging
from app.middleware.cors import configure_cors
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.request_logging import RequestLoggingMiddleware

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging(debug=settings.DEBUG)
    init_database()
    # Dev: create_all bootstraps the schema. Prod: migrations own the schema,
    # so we only seed reference data (see init_db docstring).
    await init_db(create_tables=settings.DEBUG)
    yield
    await close_db()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version="0.1.0",
        lifespan=lifespan,
    )

    # ── Exception handlers ──
    app.add_exception_handler(AppException, app_exception_handler)

    # ── Middleware ──
    app.add_middleware(RequestLoggingMiddleware)

    # Rate limiting (skips itself when Redis is unreachable — never blocks traffic)
    try:
        import redis.asyncio as aioredis
        redis_client = aioredis.from_url(
            settings.REDIS_URL, decode_responses=True, socket_connect_timeout=2
        )
    except Exception as exc:
        logger.warning("Redis unavailable, rate limiting disabled: %s", exc)
        redis_client = None

    if redis_client is not None:
        app.add_middleware(
            RateLimitMiddleware,
            redis_client=redis_client,
            max_requests=settings.RATE_LIMIT_MAX_REQUESTS,
            window_seconds=settings.RATE_LIMIT_WINDOW_SECONDS,
        )

    configure_cors(app)

    # ── Routers ──
    from app.api.v1.router import router as v1_router
    app.include_router(v1_router, prefix=settings.API_V1_PREFIX)

    # ── Health ──
    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app


app = create_app()
