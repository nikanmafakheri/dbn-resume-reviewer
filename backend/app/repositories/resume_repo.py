"""Resume repository."""

from uuid import UUID
from sqlalchemy import select
from app.domain.models.resume import Resume
from app.repositories.base import BaseRepository


class ResumeRepository(BaseRepository[Resume]):
    model = Resume

    async def list_by_user(self, user_id: UUID, skip: int = 0, limit: int = 20):
        q = (
            select(Resume)
            .where(Resume.user_id == str(user_id))
            .offset(skip)
            .limit(limit)
            .order_by(Resume.created_at.desc())
        )
        result = await self.session.execute(q)
        return result.scalars().all()
