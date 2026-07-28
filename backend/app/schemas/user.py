"""User schemas."""

from uuid import UUID

from pydantic import BaseModel, EmailStr
from app.core.constants import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None


class UserResponse(BaseModel):
    id: UUID
    email: str
    full_name: str | None
    role: UserRole
    is_active: bool

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    full_name: str | None = None
