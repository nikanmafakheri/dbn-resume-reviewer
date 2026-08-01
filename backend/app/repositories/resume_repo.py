"""Resume repository."""

from sqlalchemy import select

from app.domain.models.resume import Resume
from app.repositories.base import BaseRepository


class ResumeRepository(BaseRepository[Resume]):
    model = Resume

    async def list_all(self, skip: int = 0, limit: int = 50):
        q = (
            select(Resume)
            .offset(skip)
            .limit(limit)
            .order_by(Resume.created_at.desc())
        )
        result = await self.session.execute(q)
        return result.scalars().all()
