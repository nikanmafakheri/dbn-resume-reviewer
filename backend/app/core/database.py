"""Database configuration: async engine, session factory, lifecycle helpers."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings
from app.domain.models.base import Base


class Database:
    """Manages the async SQLAlchemy engine and session factory."""

    def __init__(self, url: str):
        self.engine = self._create_engine(url)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autoflush=False,
        )

    @staticmethod
    def _create_engine(url: str):
        """Create async SQLAlchemy engine with sensible defaults."""
        from sqlalchemy.ext.asyncio import create_async_engine

        return create_async_engine(
            str(url),
            echo=False,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=10,
            pool_recycle=300,
        )

    @property
    def engine(self):
        return self._engine

    @engine.setter
    def engine(self, value):
        self._engine = value

    def get_session_factory(self):
        return self.session_factory

    async def init_db(self) -> None:
        """Create all tables defined by SQLAlchemy models."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

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
    """FastAPI dependency: yield an async DB session."""
    db = get_database()
    async with db.session_factory() as session:
        yield session


async def init_db() -> None:
    """Initialize DB tables (called on app startup)."""
    db = get_database()
    await db.init_db()


async def close_db() -> None:
    """Dispose the engine (called on app shutdown)."""
    global _database
    if _database is not None:
        await _database.close()
        _database = None