"""Analysis schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.core.constants import AnalysisStatus


class ScoreResult(BaseModel):
    overall_score: float
    ats_score: float
    grammar_score: float
    recruiter_score: float
    summary: str
    feedback: dict = {}


class AnalysisResponse(BaseModel):
    id: UUID
    resume_id: UUID
    status: AnalysisStatus
    overall_score: float | None
    ats_score: float | None
    grammar_score: float | None
    recruiter_score: float | None
    summary: str | None
    feedback: dict = {}
    error_message: str | None
    created_at: datetime

    model_config = {"from_attributes": True}

    @classmethod
    def model_validate(cls, obj, *, strict=None, from_attributes=None, context=None, by_alias=None):
        """Map the DB `feedback_json` column to the `feedback` field."""
        data = super().model_validate(
            obj,
            strict=strict,
            from_attributes=from_attributes,
            context=context,
            by_alias=by_alias,
        )
        if hasattr(obj, "feedback_json"):
            data.feedback = obj.feedback_json or {}
        return data
