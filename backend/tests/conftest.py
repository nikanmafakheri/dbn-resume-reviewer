"""Test fixtures — async DB session, factories, etc."""

import pytest


@pytest.fixture
def sample_resume_text() -> str:
    return """John Doe
Software Engineer with 5 years of experience in Python and FastAPI.
"""
