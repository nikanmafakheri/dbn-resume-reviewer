"""Analysis schemas."""

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
    error_message: str | None
    created_at: str

    model_config = {"from_attributes": True}
