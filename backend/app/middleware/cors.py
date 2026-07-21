"""CORS middleware configuration."""

from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings


def configure_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=["*"],
        allow_headers=["*"],
    )
