"""DBN Standard model — the scoring rubric."""

from sqlalchemy import String, Text, Boolean, Float, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.domain.models.base import Base, TimestampMixin, UUIDMixin


class DBNStandard(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "dbn_standards"

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    version: Mapped[str] = mapped_column(String(20))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_by: Mapped[str] = mapped_column(ForeignKey("users.id"))

    criteria = relationship("DBNStandardCriterion", back_populates="standard", lazy="selectin")


class DBNStandardCriterion(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "dbn_standard_criteria"

    dbn_standard_id: Mapped[str] = mapped_column(ForeignKey("dbn_standards.id"))
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    weight: Mapped[float] = mapped_column(Float)
    max_score: Mapped[float] = mapped_column(Float)
    sort_order: Mapped[int] = mapped_column(Integer)

    standard = relationship("DBNStandard", back_populates="criteria")
