"""SQLAlchemy 2.0 declarative base and common mixins."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import CHAR, TypeDecorator, Uuid


class Base(DeclarativeBase):
    pass


class GUID(TypeDecorator):
    """GUID type: native UUID on PostgreSQL, CHAR(32) on SQLite.

    Migrations create native ``sa.Uuid()`` columns on both backends, so the
    decorator must compile to a type asyncpg can bind as a UUID — not a
    String(32) with a raw ``uuid.UUID`` object (asyncpg rejects that). On
    SQLite we store the 32-char hex form for the GUID() column type used in
    ``users`` seeding lookups.
    """

    impl = Uuid
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(Uuid())
        return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if isinstance(value, uuid.UUID):
            return value.hex if dialect.name != "postgresql" else value
        return value

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if isinstance(value, uuid.UUID):
            return value
        return uuid.UUID(value)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class UUIDMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        GUID(), primary_key=True, default=uuid.uuid4
    )
