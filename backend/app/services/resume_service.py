"""Resume management service."""

import uuid
from pathlib import Path
from uuid import UUID

from app.core.config import settings
from app.core.constants import ResumeStatus
from app.core.database import Database
from app.domain.models.resume import Resume
from app.repositories.resume_repo import ResumeRepository


def _safe_storage_name(original_filename: str) -> str:
    """Return a UUID-based storage name, preserving the extension.

    The user-supplied filename is used only for display (`original_filename`);
    the on-disk name is never derived from client input, which prevents
    path-traversal / overwrite attacks via crafted filenames.
    """
    suffix = Path(original_filename or "").suffix.lower()
    if suffix != ".pdf":
        suffix = ".pdf"
    return f"{uuid.uuid4().hex}{suffix}"


class ResumeService:
    def __init__(self, resume_repo: ResumeRepository):
        self.resume_repo = resume_repo

    async def upload(self, filename: str, content: bytes) -> Resume:
        upload_dir = settings.MEDIA_ROOT / "resumes"
        upload_dir.mkdir(parents=True, exist_ok=True)

        storage_name = _safe_storage_name(filename)
        file_path = upload_dir / storage_name
        file_path.write_bytes(content)

        resume = Resume(
            user_id=UUID(Database.ANONYMOUS_USER_ID),
            filename=storage_name,
            original_filename=filename,
            file_path=str(file_path),
            file_size_bytes=len(content),
            mime_type=_guess_mime(storage_name),
            status=ResumeStatus.PENDING,
        )
        return await self.resume_repo.save(resume)


def _guess_mime(storage_name: str) -> str:
    suffix = Path(storage_name).suffix.lower()
    return {
        ".pdf": "application/pdf",
    }.get(suffix, "application/octet-stream")
