"""DBN Standard model — the scoring rubric."""

from uuid import UUID

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.models.base import GUID, Base, TimestampMixin, UUIDMixin


class DBNStandard(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "dbn_standards"

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    version: Mapped[str] = mapped_column(String(20))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_by: Mapped[UUID] = mapped_column(GUID(), ForeignKey("users.id"))

    criteria = relationship("DBNStandardCriterion", back_populates="standard", lazy="selectin")


class DBNStandardCriterion(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "dbn_standard_criteria"

    dbn_standard_id: Mapped[UUID] = mapped_column(GUID(), ForeignKey("dbn_standards.id"))
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    weight: Mapped[float] = mapped_column(Float)
    max_score: Mapped[float] = mapped_column(Float)
    sort_order: Mapped[int] = mapped_column(Integer)

    standard = relationship("DBNStandard", back_populates="criteria")
