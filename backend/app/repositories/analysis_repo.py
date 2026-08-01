"""Analysis repository."""

from sqlalchemy import select

from app.domain.models.analysis import Analysis
from app.repositories.base import BaseRepository


class AnalysisRepository(BaseRepository[Analysis]):
    model = Analysis

    async def list_all(self, skip: int = 0, limit: int = 50):
        q = (
            select(Analysis)
            .offset(skip)
            .limit(limit)
            .order_by(Analysis.created_at.desc())
        )
        result = await self.session.execute(q)
        return result.scalars().all()
