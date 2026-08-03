"""Resume model."""

from uuid import UUID

from sqlalchemy import JSON, BigInteger, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import ResumeStatus
from app.domain.models.base import GUID, Base, TimestampMixin, UUIDMixin


class Resume(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "resumes"
    __table_args__ = (
        # newest-first listing (list_all)
        Index("ix_resumes_created_at", "created_at"),
        # resumes for a user, filtered by status
        Index("ix_resumes_user_id_status", "user_id", "status"),
    )

    user_id: Mapped[UUID] = mapped_column(GUID(), ForeignKey("users.id"), index=True)
    filename: Mapped[str] = mapped_column(String(255))
    original_filename: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(String(512))
    file_size_bytes: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    mime_type: Mapped[str | None] = mapped_column(String(100))
    status: Mapped[ResumeStatus] = mapped_column(index=True)
    text_content: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSON, nullable=True)

    user = relationship("User", back_populates="resumes")
    analyses = relationship("Analysis", back_populates="resume", lazy="selectin")
