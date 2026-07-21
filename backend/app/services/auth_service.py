"""Authentication service."""

from app.repositories.user_repo import UserRepository
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.schemas.auth import TokenResponse


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def login(self, email: str, password: str) -> TokenResponse:
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")

        return TokenResponse(
            access_token=create_access_token(str(user.id)),
            refresh_token=create_refresh_token(str(user.id)),
        )

    async def register(self, email: str, password: str, full_name: str | None = None):
        existing = await self.user_repo.get_by_email(email)
        if existing:
            raise ValueError("Email already registered")

        from app.domain.models.user import User
        user = User(
            email=email,
            password_hash=hash_password(password),
            full_name=full_name,
            role="candidate",
        )
        return await self.user_repo.save(user)
