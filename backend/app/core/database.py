"""Database configuration: async engine, session factory, lifecycle helpers."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

import app.domain.models.analysis  # noqa: F401
import app.domain.models.dbn_standard  # noqa: F401
import app.domain.models.resume  # noqa: F401

# Import all models so they register with Base.metadata
import app.domain.models.user  # noqa: F401
from app.core.config import settings
from app.domain.models.base import Base


class Database:
    """Manages the async SQLAlchemy engine and session factory."""

    ANONYMOUS_USER_ID = "00000000-0000-0000-0000-000000000000"

    def __init__(self, url: str):
        if not url:
            raise RuntimeError(
                "DATABASE_URL is not set. Configure it in backend/.env "
                "(postgresql+asyncpg://USER:PASS@HOST.neon.tech/DB?sslmode=require) "
                "before starting the app."
            )
        self.engine = self._create_engine(url)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autoflush=False,
        )

    @staticmethod
    def _create_engine(url: str):
        """Create async SQLAlchemy engine with sensible defaults.

        Neon is serverless: connections go idle (pool_pre_ping re-establishes)
        and per-connection resources are limited (small pool, short recycle).

        asyncpg does not accept ``sslmode`` as a URL query param (Neon appends
        ``?sslmode=require``), so we strip it from the URL and set TLS via
        ``connect_args={"ssl": ...}`` instead.
        """

        connect_args: dict = {}
        from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit

        # asyncpg accepts ``ssl`` as a connect_arg but not ``sslmode``/``channel_binding``
        # as URL params (Neon appends both). ``sslmode`` maps to ``ssl``; ``channel_binding``
        # has no asyncpg equivalent, so drop it (TLS is already required via sslmode).
        PARAM_TO_CONNECT_ARG = {"sslmode": "ssl"}
        DROP_PARAMS = {"channel_binding"}
        parts = urlsplit(url)
        params = parse_qs(parts.query)
        needs_rebuild = False
        for name, arg in PARAM_TO_CONNECT_ARG.items():
            if name in params:
                connect_args[arg] = params.pop(name, ["require"])[0]
                needs_rebuild = True
        for name in DROP_PARAMS:
            if name in params:
                params.pop(name, None)
                needs_rebuild = True
        if needs_rebuild:
            query = urlencode(
                {k: v[0] for k, v in params.items()}, doseq=True
            )
            url = urlunsplit(
                (parts.scheme, parts.netloc, parts.path, query, parts.fragment)
            )

        return create_async_engine(
            str(url),
            echo=False,
            pool_pre_ping=settings.DB_POOL_PRE_PING,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_MAX_OVERFLOW,
            pool_recycle=300,
            connect_args=connect_args,
        )

    @property
    def engine(self):
        return self._engine

    @engine.setter
    def engine(self, value):
        self._engine = value

    def get_session_factory(self):
        return self.session_factory

    async def init_db(self, create_tables: bool = True) -> None:
        """Create tables (dev bootstrap) and seed defaults, idempotently.

        In production, migrations own the schema: pass ``create_tables=False``
        (e.g. after `alembic upgrade head`) and this only seeds reference data
        (anonymous user + default standard) that does not already exist.
        """
        if create_tables:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

        # Seed anonymous user and default DBN Standard
        from uuid import UUID

        from sqlalchemy import select

        from app.core.constants import UserRole
        from app.core.security import hash_password
        from app.domain.models.dbn_standard import DBNStandard, DBNStandardCriterion
        from app.domain.models.user import User

        async with self.session_factory() as session:
            # Check if anonymous user already exists
            result = await session.execute(
                select(User).where(User.id == UUID(self.ANONYMOUS_USER_ID))
            )
            if not result.scalar_one_or_none():
                anonymous = User(
                    id=UUID(self.ANONYMOUS_USER_ID),
                    email="anonymous@dbnresume.com",
                    password_hash=hash_password("anonymous"),
                    full_name="Anonymous User",
                    role=UserRole.SYSTEM,
                    is_active=True,
                )
                session.add(anonymous)
                # Flush now so the anonymous user row is committed before the
                # DBNStandard below references it via created_by (a plain FK
                # column, not an ORM relationship, so SQLAlchemy won't infer
                # the dependency ordering itself).
                await session.flush()

            # Check if default standard already exists
            result = await session.execute(
                select(DBNStandard).where(DBNStandard.name == "DBN Resume Standard v1")
            )
            if not result.scalar_one_or_none():
                standard = DBNStandard(
                    name="DBN Resume Standard v1",
                    description="Default scoring rubric for resume analysis",
                    version="1.0",
                    is_active=True,
                    created_by=UUID(self.ANONYMOUS_USER_ID),
                )
                session.add(standard)
                await session.flush()

                criteria = [
                    DBNStandardCriterion(
                        dbn_standard_id=standard.id,
                        name="Overall Score",
                        description="Composite evaluation of the entire resume",
                        weight=25.0,
                        max_score=100.0,
                        sort_order=1,
                    ),
                    DBNStandardCriterion(
                        dbn_standard_id=standard.id,
                        name="ATS Score",
                        description="Compatibility with Applicant Tracking Systems",
                        weight=25.0,
                        max_score=100.0,
                        sort_order=2,
                    ),
                    DBNStandardCriterion(
                        dbn_standard_id=standard.id,
                        name="Grammar Score",
                        description="Spelling, grammar, punctuation, and writing style",
                        weight=25.0,
                        max_score=100.0,
                        sort_order=3,
                    ),
                    DBNStandardCriterion(
                        dbn_standard_id=standard.id,
                        name="Recruiter Score",
                        description="Appeal to human recruiters — impact, clarity, achievements",
                        weight=25.0,
                        max_score=100.0,
                        sort_order=4,
                    ),
                ]
                session.add_all(criteria)

            await session.commit()

    async def close(self) -> None:
        """Dispose of the engine and all connections."""
        await self.engine.dispose()


# Global singleton
_database: "Database | None" = None


def init_database() -> "Database":
    """Initialize and return the global Database instance."""
    global _database
    if _database is None:
        _database = Database(settings.DATABASE_URL)
    return _database


def get_database() -> "Database":
    """Get the global Database instance (must be initialized first)."""
    global _database
    if _database is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")
    return _database


async def get_db() -> AsyncSession:
    """FastAPI dependency: yield an async DB session.

    Commits on success, rolls back on exception.
    """
    db = get_database()
    async with db.session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def init_db(create_tables: bool = True) -> None:
    """Initialize DB tables (called on app startup)."""
    db = get_database()
    await db.init_db(create_tables=create_tables)


async def close_db() -> None:
    """Dispose the engine (called on app shutdown)."""
    global _database
    if _database is not None:
        await _database.close()
        _database = None
