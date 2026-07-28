"""Test fixtures — async DB session, factories, etc."""

from __future__ import annotations

import asyncio
from typing import AsyncGenerator
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.main import create_app
from app.core.config import settings
from app.core.database import get_db
from app.domain.models.base import Base
from app.domain.models.user import User
from app.core.constants import AnalysisStatus, ResumeStatus, UserRole
from app.core.security import hash_password

# Use a separate test database
TEST_DATABASE_URL = settings.DATABASE_URL
if "test" not in str(TEST_DATABASE_URL):
    TEST_DATABASE_URL = str(TEST_DATABASE_URL).replace("dbn_resume", "dbn_resume_test")


@pytest.fixture(scope="session")
def event_loop():
    """Create a single event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def db_engine():
    """Create the test database engine."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
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
        yield db_session

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


@pytest_asyncio.fixture
async def auth_headers(client: AsyncClient, test_user: User) -> dict[str, str]:
    """Get JWT auth headers for the test user."""
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "TestPass123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_resume_text() -> str:
    return """John Doe
Software Engineer with 5 years of experience in Python and FastAPI.
Proficient in PostgreSQL, Redis, and cloud infrastructure.
"""