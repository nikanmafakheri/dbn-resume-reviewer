"""Application configuration via Pydantic Settings."""

from __future__ import annotations

from pathlib import Path

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
    # Required (no default): Neon Postgres is the single database. An empty
    # value makes startup fail fast rather than silently falling back to a
    # local SQLite file. Format:
    #   postgresql+asyncpg://USER:PASSWORD@HOST.neon.tech/DB?sslmode=require
    DATABASE_URL: str = ""
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_PRE_PING: bool = True
    # Neon requires TLS; asyncpg honors `sslmode` in the URL/connect_args.
    DATABASE_SSL_MODE: str = "require"

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
    # InferX is the single LLM provider — an OpenAI-compatible gateway at
    # model.inferx.net running DeepSeek V4 Flash.

    # Per-provider ceiling on a single LLM request (seconds). Applied around each
    # `generate()` call in the scorer, so a slow/hung provider fails gracefully
    # (classified `timed_out` → friendly wait-and-retry) instead of leaving the
    # frontend polling a stuck `processing` analysis forever. Sits above normal
    # latency but well below a user's patience.
    LLM_REQUEST_TIMEOUT_SECONDS: float = 90.0
    INFERX_API_KEY: str | None = None
    INFERX_BASE_URL: str = "https://model.inferx.net/endpoints/v1"
    INFERX_MODEL: str = "Qwen3.6-35B-A3B-FP8"

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

    @field_validator("DATABASE_URL", mode="after")
    @classmethod
    def normalize_database_url(cls, v: str) -> str:
        """Enforce the Postgres/Neon contract on DATABASE_URL.

        - Empty is allowed here so the module imports and unit tests construct
          Settings freely; the engine raises a clear error at startup instead
          (see ``app.core.database.Database``).
        - Only an asyncpg Postgres URL is supported. Migrations and tests swap
          the database name on this string, so a non-Postgres scheme would
          corrupt the test DB derivation — reject it loudly.
        - Neon's connection string includes ``?sslmode=require``. asyncpg does
          not accept ``sslmode`` as a URL query param, so we validate it stays
          well-formed but leave SSL translation to the engine
          (``app.core.database``), which moves it into ``connect_args``.
        """
        if not v:
            return v
        if not v.startswith("postgresql") or "+asyncpg" not in v:
            raise ValueError(
                "DATABASE_URL must use the asyncpg driver (e.g. "
                "postgresql+asyncpg://USER:PASS@HOST.neon.tech/DB?sslmode=require). "
                f"Got: {v!r}"
            )
        return v

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
