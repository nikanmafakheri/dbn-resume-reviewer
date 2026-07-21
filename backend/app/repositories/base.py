"""Generic CRUD base repository."""

from collections.abc import Sequence
from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository[T]:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: UUID) -> T | None:
        return await self.session.get(self.model, id)

    async def list(self, skip: int = 0, limit: int = 20) -> tuple[Sequence[T], int]:
        count_q = select(func.count()).select_from(self.model)
        total = (await self.session.execute(count_q)).scalar_one()

        q = select(self.model).offset(skip).limit(limit)
        result = (await self.session.execute(q)).scalars().all()
        return result, total

    async def save(self, instance: T) -> T:
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def delete(self, instance: T) -> None:
        await self.session.delete(instance)
