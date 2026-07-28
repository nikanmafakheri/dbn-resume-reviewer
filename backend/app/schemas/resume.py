"""Resume schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from app.core.constants import ResumeStatus


class ResumeResponse(BaseModel):
    id: UUID
    filename: str
    original_filename: str
    file_size_bytes: int | None
    mime_type: str | None
    status: ResumeStatus
    created_at: datetime

    model_config = {"from_attributes": True}
