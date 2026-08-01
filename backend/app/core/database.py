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
        self.engine = self._create_engine(url)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autoflush=False,
        )

    @staticmethod
    def _create_engine(url: str):
        """Create async SQLAlchemy engine with sensible defaults."""

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
