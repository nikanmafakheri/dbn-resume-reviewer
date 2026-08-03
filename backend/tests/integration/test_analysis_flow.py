"""End-to-end test of the upload → analyze → fetch analysis flow.

Verifies the critical scoring-pipeline contract: the scorer is injected and
its failures surface as `failed` + `error_message` (never silently swallowed).
The LLM provider is stubbed so the test is deterministic and offline.
"""

from uuid import uuid4

import pytest

from app.core.constants import AnalysisStatus, UserRole
from app.core.database import Database
from app.core.scoring import weighted_overall
from app.domain.models.resume import Resume
from app.domain.models.user import User
from app.schemas.analysis import Confidence, DimensionScore, ScoreResult


def _fake_result() -> ScoreResult:
    """A fully-valid, deterministic ScoreResult for the scoring contract."""
    dimensions = {
        name: DimensionScore(
            score=score,
            justification=(
                f"A defensible justification for the {name} dimension that is long enough."
            ),
        )
        for name, score in {
            "ats": 72.0,
            "skills": 85.0,
            "experience": 88.0,
            "formatting": 91.0,
            "content": 80.0,
        }.items()
    }
    return ScoreResult(
        dimensions=dimensions,
        overall=weighted_overall({name: d.score for name, d in dimensions.items()}),
        confidence=Confidence(label="high", score=1.0, justifications_valid=5),
        strengths=["Clear structure", "Strong Python expertise"],
        weaknesses=["Few quantified metrics"],
        missing_skills=["Kubernetes"],
        actionable_recommendations=["Add quantified impact to 2023 role"],
        summary="Strong resume overall.",
        summary_en="Strong resume overall.",
        analysis_fa=(
            "رزومه ساختار منظمی دارد و تجربه فنی به‌خوبی مستند شده است؛ اما "
            "می‌تواند با افزودن معیارهای کمی تأثیرگذاری بیشتری داشته باشد."
        ),
    )


class FakeScorer:
    """Deterministic stand-in for ResumeScorer."""

    def __init__(self, result: ScoreResult | None = None, exc: Exception | None = None):
        self.result = result
        self.exc = exc

    async def score(self, resume_text: str) -> ScoreResult:
        if self.exc is not None:
            raise self.exc
        return self.result or _fake_result()


async def _seed_resume(db_session) -> str:
    anon = User(
        id=Database.ANONYMOUS_USER_ID,
        email="anonymous@dbnresume.com",
        password_hash="x",
        full_name="Anonymous",
        role=UserRole.SYSTEM,
        is_active=True,
    )
    db_session.add(anon)
    await db_session.flush()

    resume = Resume(
        id=uuid4(),
        user_id=Database.ANONYMOUS_USER_ID,
        filename="resume.pdf",
        original_filename="resume.pdf",
        file_path="/tmp/nonexistent.pdf",
        file_size_bytes=1024,
        mime_type="application/pdf",
        status="pending",
        text_content="Software engineer with 5 years Python experience.",
    )
    db_session.add(resume)
    await db_session.flush()
    return str(resume.id)


@pytest.mark.asyncio
async def test_upload_and_analyze_flow(client, db_session, monkeypatch):
    """A healthy scorer completes the analysis inline."""
    resume_id = await _seed_resume(db_session)
    monkeypatch.setattr("app.dependencies.create_scorer", lambda: FakeScorer())

    resp = await client.post(f"/api/v1/resumes/{resume_id}/analyze")
    assert resp.status_code == 202

    body = resp.json()
    assert body["id"] is not None
    assert body["status"] == AnalysisStatus.COMPLETED
    # Overall is the deterministic weighted mean of the dimensions.
    assert body["overall_score"] == pytest.approx(82.35, abs=0.01)
    assert body["ats_score"] == 72.0
    assert body["skills_score"] == 85.0
    assert body["experience_score"] == 88.0
    assert body["formatting_score"] == 91.0
    assert body["content_score"] == 80.0
    assert body["summary"] == "Strong resume overall."
    assert body["summary_en"] == "Strong resume overall."
    assert body["analysis_fa"].startswith("رزومه")
    assert body["scores_json"]["dimensions"]["ats"]["score"] == 72.0
    assert body["scores_json"]["dimensions"]["ats"]["justification"]
    assert body["scores_json"]["confidence"]["label"] == "high"


@pytest.mark.asyncio
async def test_scoring_failure_surfaces_error(client, db_session, monkeypatch):
    """A failing scorer must set FAILED + error_message, never 500."""
    resume_id = await _seed_resume(db_session)
    monkeypatch.setattr(
        "app.dependencies.create_scorer",
        lambda: FakeScorer(exc=RuntimeError("LLM provider down")),
    )

    resp = await client.post(f"/api/v1/resumes/{resume_id}/analyze")
    assert resp.status_code == 202

    body = resp.json()
    assert body["status"] == AnalysisStatus.FAILED
    assert body["error_message"] == "LLM provider down"


@pytest.mark.asyncio
async def test_invalid_uuid_returns_422_not_500(client):
    """Path params are validated as UUID — malformed input gets a 422."""
    resp = await client.post("/api/v1/resumes/not-a-uuid/analyze")
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_analyze_missing_resume_returns_404(client):
    resp = await client.post(f"/api/v1/resumes/{uuid4()}/analyze")
    assert resp.status_code == 404
