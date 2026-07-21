"""Analysis repository."""

from uuid import UUID
from sqlalchemy import select
from app.domain.models.analysis import Analysis
from app.repositories.base import BaseRepository


class AnalysisRepository(BaseRepository[Analysis]):
    model = Analysis

    async def list_by_user(self, user_id: UUID, skip: int = 0, limit: int = 20):
        q = (
            select(Analysis)
            .where(Analysis.user_id == str(user_id))
            .offset(skip)
            .limit(limit)
            .order_by(Analysis.created_at.desc())
        )
        result = await self.session.execute(q)
        return result.scalars().all()
