"""User model."""

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.models.base import Base, TimestampMixin, UUIDMixin


class User(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str | None] = mapped_column(String(255))
    # Role is stored as VARCHAR(50) (see migration 0001); keep the column a
    # String so SQLAlchemy doesn't create a native Postgres ENUM type that the
    # migration never made (would break asyncpg on `INSERT INTO users`).
    role: Mapped[str] = mapped_column(String(50), index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    resumes = relationship("Resume", back_populates="user", lazy="selectin")
