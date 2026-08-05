"""Analysis schemas — strict JSON contract for the DBN scoring pipeline.

Every score an LLM emits is justified per dimension and the DBN Overall Score is
a *deterministic weighted function* of the five component dimensions (see
``app/core/scoring.py``). The AI never supplies an arbitrary overall value; it
supplies evidence, and the scorer computes the overall from the weights.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

from app.core.constants import AnalysisStatus

#: Score range is 0-100 inclusive.
SCORE_MIN = 0.0
SCORE_MAX = 100.0

#: Dimensions the LLM must justify, and the exact keys returned in JSON.
DIMENSIONS = ("ats", "skills", "experience", "formatting", "content")

#: Canonical (key, label) pairs for serialization.
DIMENSION_LABELS: tuple[tuple[str, str], ...] = (
    ("ats", "ATS Compatibility"),
    ("skills", "Skills"),
    ("experience", "Experience"),
    ("formatting", "Formatting"),
    ("content", "Content Quality"),
)


class DimensionScore(BaseModel):
    """One dimension's score plus the evidence that justifies it."""

    score: float = Field(ge=SCORE_MIN, le=SCORE_MAX, description="0-100 score")
    justification: str = Field(
        min_length=20,
        description="Evidence-based rationale: what was found, what was missing, why this score.",
    )


class Confidence(BaseModel):
    """Structural confidence — how much of the requested schema validated."""

    label: Literal["low", "medium", "high"]
    score: float = Field(ge=0.0, le=1.0)
    justifications_valid: int = Field(ge=0)
    note: str = Field(default="")


class ScoreResult(BaseModel):
    """Full validated result of a resume evaluation.

    ``overall`` is recomputed by the scorer from the dimension scores via the
    documented weighted formula — it is not read from the LLM response.
    """

    dimensions: dict[str, DimensionScore] = Field(
        min_length=len(DIMENSIONS), max_length=len(DIMENSIONS)
    )
    overall: float = Field(ge=SCORE_MIN, le=SCORE_MAX)
    confidence: Confidence
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    actionable_recommendations: list[str] = Field(default_factory=list)
    summary: str = Field(default="", min_length=0)
    summary_en: str = Field(default="", min_length=0)
    analysis_fa: str = Field(default="", min_length=0)


class AnalysisResponse(BaseModel):
    """API response — flat top-level scalar scores plus the full nested result.

    Legacy scalar columns (``grammar_score``, ``recruiter_score``) are kept so
    historical analyses remain readable; new analyses store the full result in
    ``scores_json``.
    """

    id: UUID
    resume_id: UUID
    status: AnalysisStatus
    overall_score: float | None
    ats_score: float | None
    skills_score: float | None
    experience_score: float | None
    formatting_score: float | None
    content_score: float | None
    grammar_score: float | None
    recruiter_score: float | None
    summary: str | None
    summary_en: str | None = None
    analysis_fa: str | None = None
    feedback: dict = {}
    scores_json: dict | None = None
    error_message: str | None
    error_code: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}

    @classmethod
    def model_validate(cls, obj, *, strict=None, from_attributes=None, context=None, by_alias=None):
        """Map DB columns/JSON into the response shape.

        Flat dimension scalars come from either the dedicated columns (if set)
        or the nested ``scores_json`` dict (new-style analyses), and
        ``feedback_json`` maps to ``feedback``.
        """
        data = super().model_validate(
            obj,
            strict=strict,
            from_attributes=from_attributes,
            context=context,
            by_alias=by_alias,
        )
        scores_json = getattr(obj, "scores_json", None) or {}
        if not isinstance(scores_json, dict):
            scores_json = {}
        dimensions = scores_json.get("dimensions") or {}

        for key in ("ats", "skills", "experience", "formatting", "content"):
            current = getattr(data, f"{key}_score", None)
            if current is None:
                dim = dimensions.get(key) or {}
                if isinstance(dim, dict) and isinstance(dim.get("score"), (int, float)):
                    setattr(data, f"{key}_score", float(dim["score"]))

        if hasattr(obj, "feedback_json"):
            data.feedback = obj.feedback_json or {}
        if hasattr(obj, "scores_json") and obj.scores_json is not None:
            data.scores_json = obj.scores_json
        return data
