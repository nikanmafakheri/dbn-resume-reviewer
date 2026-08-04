"""Analysis model — flat legacy score columns plus nested result JSON.

New-style analyses store the complete, validated result (dimensions with
justifications, confidence, strengths/weaknesses/recommendations) in
``scores_json`` and mirror the six scores into dedicated columns for cheap
querying/filtering. Legacy ``grammar_score`` / ``recruiter_score`` columns are
kept so historical rows remain readable.
"""

from uuid import UUID

from sqlalchemy import JSON, Float, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.models.base import GUID, Base, TimestampMixin, UUIDMixin


class Analysis(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "analyses"
    __table_args__ = (
        # newest-first listing (list_all)
        Index("ix_analyses_created_at", "created_at"),
        # analyses for a given resume, newest first
        Index("ix_analyses_resume_id_created_at", "resume_id", "created_at"),
    )

    resume_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("resumes.id"), index=True
    )
    user_id: Mapped[UUID] = mapped_column(GUID(), ForeignKey("users.id"), index=True)
    dbn_standard_id: Mapped[UUID | None] = mapped_column(
        GUID(), ForeignKey("dbn_standards.id"), nullable=True, index=True
    )
    # Stored as VARCHAR (see migration 0002); keep String so SQLAlchemy doesn't
    # create a native Postgres ENUM type the migration never made.
    status: Mapped[str] = mapped_column(String(50), index=True)
    overall_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    ats_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    # New dimension columns (mirror of scores_json.dimensions.*.score).
    skills_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    experience_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    formatting_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    content_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    # Legacy MVP dimensions — retained for backward compatibility only.
    grammar_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    recruiter_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    summary_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    analysis_fa: Mapped[str | None] = mapped_column(Text, nullable=True)
    feedback_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    # Full nested evaluation result (dimensions, confidence, lists, summary).
    scores_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    processing_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)

    resume = relationship("Resume", back_populates="analyses")
