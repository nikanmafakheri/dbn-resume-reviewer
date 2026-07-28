"""User profile routes."""

from fastapi import APIRouter, Depends

from app.dependencies import get_current_user, get_user_service
from app.domain.models.user import User
from app.services.user_service import UserService
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_profile(
    current_user: User = Depends(get_current_user),
):
    """Return the authenticated user's profile."""
    return UserResponse.model_validate(current_user)


@router.patch("/me", response_model=UserResponse)
async def update_profile(
    body: UserUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    """Update the authenticated user's profile."""
    updated = await user_service.update_profile(
        str(current_user.id),
        full_name=body.full_name,
    )
    return UserResponse.model_validate(updated)
