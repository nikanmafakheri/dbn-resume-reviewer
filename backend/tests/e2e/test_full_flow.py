"""Full-stack e2e flow: multipart upload → analyze → poll result.

Drives the real HTTP API over an ASGI transport (no route bypassed). The
scorer is stubbed so the flow is deterministic and offline — a live LLM call
is exercised manually (see Todo: Gemini quota retest).

Flow under test:
  1. POST /api/v1/resumes/upload       (real multipart file)
  2. POST /api/v1/resumes/{id}/analyze (inline scoring, stubbed scorer)
  3. GET  /api/v1/analysis/{id}        (poll until completed)
  4. GET  /api/v1/dbn-standards/template/download  (template serves a .pptx)
"""

from __future__ import annotations

import asyncio
from uuid import uuid4

import pytest

from app.core.constants import AnalysisStatus


def _text_pdf_bytes() -> bytes:
    """Build a small, valid PDF containing extractable text.

    Uses PyMuPDF (the same library the app uses) so the upload route's PDF
    extraction succeeds and returns non-empty ``text_content``.
    """
    import fitz  # PyMuPDF

    doc = fitz.open()
    page = doc.new_page()
    page.insert_text(
        (72, 72),
        "Software engineer with 5 years of Python and FastAPI experience.",
    )
    return doc.tobytes()


class FakeScorer:
    """Deterministic stand-in for ResumeScorer (offline, no LLM)."""

    async def score(self, resume_text: str):
        from app.core.scoring import weighted_overall
        from app.schemas.analysis import Confidence, DimensionScore, ScoreResult

        dimensions = {
            name: DimensionScore(
                score=score,
                justification=(
                    f"A defensible justification for {name} that is long enough "
                    "to satisfy the parser's quality bar."
                ),
            )
            for name, score in {
                "ats": 75.0,
                "skills": 80.0,
                "experience": 85.0,
                "formatting": 90.0,
                "content": 78.0,
            }.items()
        }
        return ScoreResult(
            dimensions=dimensions,
            overall=weighted_overall({n: d.score for n, d in dimensions.items()}),
            confidence=Confidence(label="high", score=1.0, justifications_valid=5),
            strengths=["Strong FastAPI experience"],
            weaknesses=["No quantified metrics"],
            missing_skills=["Docker"],
            actionable_recommendations=["Add impact numbers to the 2023 role"],
            summary="Strong engineering resume.",
            summary_en="Strong engineering resume.",
            analysis_fa="رزومه خوبی است اما می‌تواند معیارهای کمی بیشتری داشته باشد.",
        )


@pytest.mark.asyncio
async def test_upload_analyze_poll_template_flow(client, db_session, monkeypatch):
    """The complete user journey over the real API."""
    monkeypatch.setattr("app.dependencies.create_scorer", lambda: FakeScorer())

    # 1. Upload a real multipart PDF with extractable text (generated with
    # PyMuPDF so the extraction path actually runs and returns text).
    pdf_bytes = _text_pdf_bytes()
    upload = await client.post(
        "/api/v1/resumes/upload",
        files={
            "file": (
                "resume.pdf",
                pdf_bytes,
                "application/pdf",
            )
        },
    )
    assert upload.status_code == 201, upload.text
    resume_id = upload.json()["id"]
    assert upload.json()["original_filename"] == "resume.pdf"

    # 2. Trigger analysis (inline, stubbed scorer).
    analyze = await client.post(f"/api/v1/resumes/{resume_id}/analyze")
    assert analyze.status_code == 202
    analysis_id = analyze.json()["id"]
    assert analyze.json()["status"] == AnalysisStatus.COMPLETED

    # 3. Poll the analysis result (already completed in the inline path).
    for _ in range(20):
        result = await client.get(f"/api/v1/analysis/{analysis_id}")
        assert result.status_code == 200
        body = result.json()
        if body["status"] in (AnalysisStatus.COMPLETED, AnalysisStatus.FAILED):
            break
        await asyncio.sleep(0.05)
    assert body["status"] == AnalysisStatus.COMPLETED, body
    assert body["overall_score"] is not None
    assert body["analysis_fa"].startswith("رزومه")
    assert body["scores_json"]["confidence"]["label"] == "high"

    # 4. Template download serves a real .pptx.
    template = await client.get("/api/v1/dbn-standards/template/download")
    assert template.status_code == 200
    assert (
        template.headers["content-type"]
        == "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )


@pytest.mark.asyncio
async def test_upload_rejects_bad_type_and_oversize(client, db_session):
    """Validation gates on upload: bad extension and oversize file."""
    bad_ext = await client.post(
        "/api/v1/resumes/upload",
        files={"file": ("resume.exe", b"MZ....", "application/octet-stream")},
    )
    assert bad_ext.status_code == 400

    oversize = await client.post(
        "/api/v1/resumes/upload",
        files={"file": ("big.pdf", b"x" * (11 * 1024 * 1024), "application/pdf")},
    )
    assert oversize.status_code == 400


@pytest.mark.asyncio
async def test_list_and_delete_resume(client, db_session):
    """Upload → list → delete round-trip."""
    upload = await client.post(
        "/api/v1/resumes/upload",
        files={"file": ("a.pdf", b"%PDF-1.4\n%%EOF\n", "application/pdf")},
    )
    assert upload.status_code == 201
    resume_id = upload.json()["id"]

    listed = await client.get("/api/v1/resumes")
    assert listed.status_code == 200
    assert any(r["id"] == resume_id for r in listed.json())

    deleted = await client.delete(f"/api/v1/resumes/{resume_id}")
    assert deleted.status_code == 204

    # Confirm the resume is gone from the list.
    listed_after = await client.get("/api/v1/resumes")
    assert listed_after.status_code == 200
    assert not any(r["id"] == resume_id for r in listed_after.json())

    # Deletion of a non-existent resume → 404.
    missing = await client.delete(f"/api/v1/resumes/{uuid4()}")
    assert missing.status_code == 404
