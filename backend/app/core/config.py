"""Application configuration via Pydantic Settings."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# .env lives at the backend project root (sibling of the `app/` package).
# Resolve it absolutely so startup never depends on the CWD (Docker workers,
# pytest, systemd, etc.).
_BACKEND_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_BACKEND_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        # Ignore legacy/extra env vars (e.g. old JWT settings) instead of
        # crashing startup on an outdated .env.
        extra="ignore",
    )

    # ── App ──────────────────────────────────────────
    APP_NAME: str = "DBN Resume Reviewer"
    APP_URL: str = "http://localhost:8000"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # ── Security ─────────────────────────────────────
    # Dev-only default so a fresh checkout boots without a .env. Override in
    # production via the SECRET_KEY env var — never ship the default.
    SECRET_KEY: str = "dev-only-insecure-secret-change-me"

    # ── Database ─────────────────────────────────────
    DATABASE_URL: str = "sqlite+aiosqlite:///./dbn_resume.db"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_PRE_PING: bool = True

    # ── Redis ────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"
    RATE_LIMIT_MAX_REQUESTS: int = 60
    RATE_LIMIT_WINDOW_SECONDS: int = 60

    # ── Media / Uploads ──────────────────────────────
    MEDIA_ROOT: Path = Path("media")

    # ── Standard template download ───────────────────
    # Path to the downloadable DBN Standard resume template (.pptx). Relative
    # paths resolve against the repo root (one level above the backend/ pkg),
    # so this is `dbn-standard-resume-template/<file>.pptx`.
    TEMPLATE_PPTX_PATH: Path = Path(
        "dbn-standard-resume-template/Black and White Minimalist Professional Resume A4.pptx"
    )

    # ── CORS ─────────────────────────────────────────
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    CORS_ALLOW_CREDENTIALS: bool = True

    # ── LLM Provider ─────────────────────────────────
    LLM_PROVIDER: Literal["gemini", "openai", "claude", "openrouter"] = "gemini"
    GEMINI_MODEL: str = "gemini-2.0-flash"
    GEMINI_API_KEY: str | None = None
    OPENAI_API_KEY: str | None = None
    CLAUDE_API_KEY: str | None = None
    OPENROUTER_API_KEY: str | None = None

    # ── Email ────────────────────────────────────────
    SMTP_HOST: str | None = None
    SMTP_PORT: int = 587
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAIL_FROM: str = "noreply@dbnresume.com"

    # ── Celery ───────────────────────────────────────
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # ── Idempotency ──────────────────────────────────
    IDEMPOTENCY_TTL: int = 86_400  # 24 hours

    @field_validator("MEDIA_ROOT", mode="before")
    @classmethod
    def resolve_media_root(cls, v: str | Path) -> Path:
        path = Path(v)
        if not path.is_absolute():
            path = _BACKEND_ROOT / path
        return path.resolve()

    @field_validator("TEMPLATE_PPTX_PATH", mode="before")
    @classmethod
    def resolve_template_pptx(cls, v: str | Path) -> Path:
        path = Path(v)
        if not path.is_absolute():
            # Template lives at the repo root (one level above backend/).
            path = _BACKEND_ROOT.parent / path
        return path.resolve()


settings = Settings()  # type: ignore[call-arg]
