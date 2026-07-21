"""DBN Standard repository."""

from sqlalchemy import select
from app.domain.models.dbn_standard import DBNStandard
from app.repositories.base import BaseRepository


class DBNStandardRepository(BaseRepository[DBNStandard]):
    model = DBNStandard

    async def get_active(self) -> DBNStandard | None:
        q = select(DBNStandard).where(DBNStandard.is_active == True)
        return (await self.session.execute(q)).scalar_one_or_none()
