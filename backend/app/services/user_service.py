"""User management service."""

from app.repositories.user_repo import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def get_profile(self, user_id: str):
        return await self.user_repo.get_by_id(user_id)

    async def update_profile(self, user_id: str, full_name: str | None = None):
        user = await self.user_repo.get_by_id(user_id)
        if full_name is not None:
            user.full_name = full_name
        return user
