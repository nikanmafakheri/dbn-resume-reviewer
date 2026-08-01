"""Analysis model — includes flat score columns for MVP."""

from uuid import UUID

from sqlalchemy import JSON, Float, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import AnalysisStatus
from app.domain.models.base import GUID, Base, TimestampMixin, UUIDMixin


class Analysis(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "analyses"

    resume_id: Mapped[UUID] = mapped_column(GUID(), ForeignKey("resumes.id"))
    user_id: Mapped[UUID] = mapped_column(GUID(), ForeignKey("users.id"))
    dbn_standard_id: Mapped[UUID | None] = mapped_column(
        GUID(), ForeignKey("dbn_standards.id"), nullable=True
    )
    status: Mapped[AnalysisStatus]
    overall_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    ats_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    grammar_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    recruiter_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    feedback_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    processing_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)

    resume = relationship("Resume", back_populates="analyses")
