"""User repository."""

from uuid import UUID

from sqlalchemy import select

from app.domain.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User

    async def get_by_email(self, email: str) -> User | None:
        q = select(User).where(User.email == email)
        return (await self.session.execute(q)).scalar_one_or_none()

    async def get_by_id(self, id: UUID) -> User | None:
        return await self.get(id)
