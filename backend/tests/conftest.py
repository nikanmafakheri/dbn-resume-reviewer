"""Test fixtures — async DB session, factories, etc."""

from __future__ import annotations

import os
from typing import AsyncGenerator
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.config import settings
from app.core.constants import UserRole
from app.core.database import get_db
from app.core.security import hash_password
from app.domain.models.base import Base
from app.domain.models.user import User
from app.main import create_app

# Use a separate test database.
# Prefer an explicit TEST_DATABASE_URL (set in CI / local Neon testing) so the
# suite can target a dedicated database without string surgery on a Neon URL.
# Fall back to deriving `dbn_resume_test` from DATABASE_URL. On Neon the test
# database must already exist; the session-scoped create_all/drop_all only
# (re)builds tables, it does not create the database.
_TEST_DB_URL = os.environ.get("TEST_DATABASE_URL", "")
if not _TEST_DB_URL:
    _TEST_DB_URL = str(settings.DATABASE_URL)
    if "test" not in _TEST_DB_URL:
        _TEST_DB_URL = _TEST_DB_URL.replace("dbn_resume", "dbn_resume_test")

if "test" not in _TEST_DB_URL:
    raise RuntimeError(
        "Refusing to run the test suite against a non-test database "
        f"({_TEST_DB_URL!r}). Set TEST_DATABASE_URL to a dedicated test DB "
        "(e.g. the 'dbn_resume_test' database on Neon)."
    )
if "+asyncpg" not in _TEST_DB_URL:
    raise RuntimeError(
        "Tests require a PostgreSQL database (asyncpg). "
        f"Got non-Postgres URL: {_TEST_DB_URL!r}"
    )

TEST_DATABASE_URL = _TEST_DB_URL


@pytest_asyncio.fixture(scope="session")
async def db_engine():
    """Create the test database engine.

    Reuses the app's engine factory so tests exercise the exact same
    connect_args / SSL / pool behavior as production (asyncpg + Neon).
    """
    from app.core.database import Database

    engine = Database._create_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Seed reference rows (anonymous user + default DBN standard) like prod's
    # init_db: Postgres enforces FKs, so the upload/analyze routes need the
    # ANONYMOUS_USER_ID row present before they reference it. (SQLite let this
    # pass without FK enforcement.)
    anon_id = UUID(Database.ANONYMOUS_USER_ID)
    factory = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)
    async with factory() as session:
        from app.core.constants import UserRole
        from app.core.security import hash_password
        from app.domain.models.user import User

        if not await session.get(User, anon_id):
            session.add(
                User(
                    id=anon_id,
                    email="anonymous@dbnresume.com",
                    password_hash=hash_password("anonymous"),
                    full_name="Anonymous User",
                    role=UserRole.SYSTEM,
                    is_active=True,
                )
            )
            await session.commit()

    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(db_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a fresh test DB session per test."""
    session_factory = async_sessionmaker(
        bind=db_engine, expire_on_commit=False, autoflush=False
    )
    async with session_factory() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """FastAPI test client with in-memory DB overrides."""

    app = create_app()

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        try:
            yield db_session
            await db_session.flush()
        except Exception:
            await db_session.rollback()
            raise

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(db_session: AsyncSession) -> User:
    """Create a test user."""
    user = User(
        id=uuid4(),
        email="test@example.com",
        password_hash=hash_password("TestPass123"),
        full_name="Test User",
        role=UserRole.CANDIDATE,
        is_active=True,
    )
    db_session.add(user)
    await db_session.flush()
    return user


@pytest.fixture
def sample_resume_text() -> str:
    return """John Doe
Software Engineer with 5 years of experience in Python and FastAPI.
Proficient in PostgreSQL, Redis, and cloud infrastructure.
"""
