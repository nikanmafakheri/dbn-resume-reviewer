"""Resume schemas."""

from pydantic import BaseModel
from app.core.constants import ResumeStatus


class ResumeResponse(BaseModel):
    id: str
    filename: str
    original_filename: str
    file_size_bytes: int | None
    mime_type: str | None
    status: ResumeStatus
    created_at: str

    model_config = {"from_attributes": True}
