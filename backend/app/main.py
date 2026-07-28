"""FastAPI application factory."""

from contextlib import asynccontextmanager

from fastapi import FastAPI  # type: ignore[import-not-found]

from app.core.config import settings
from app.core.logging import configure_logging
from app.core.database import init_database, init_db, close_db
from app.core.exceptions import AppException, app_exception_handler
from app.middleware.cors import configure_cors
from app.middleware.request_logging import RequestLoggingMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging(debug=settings.DEBUG)
    init_database()
    await init_db()
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
