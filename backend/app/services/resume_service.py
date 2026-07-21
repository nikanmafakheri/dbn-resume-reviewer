"""Resume management service."""

from pathlib import Path
from uuid import UUID
from app.core.config import settings
from app.repositories.resume_repo import ResumeRepository
from app.domain.models.resume import Resume
from app.core.constants import ResumeStatus


class ResumeService:
    def __init__(self, resume_repo: ResumeRepository):
        self.resume_repo = resume_repo

    async def upload(self, user_id: UUID, filename: str, content: bytes) -> Resume:
        upload_dir = settings.MEDIA_ROOT / "resumes"
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_path = upload_dir / filename
        file_path.write_bytes(content)

        resume = Resume(
            user_id=str(user_id),
            filename=filename,
            original_filename=filename,
            file_path=str(file_path),
            file_size_bytes=len(content),
            status=ResumeStatus.PENDING,
        )
        return await self.resume_repo.save(resume)
