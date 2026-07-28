"""Authentication routes: register, login, refresh."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_auth_service
from app.services.auth_service import AuthService
from app.schemas.auth import LoginRequest, TokenResponse, RefreshRequest
from app.schemas.user import UserCreate, UserResponse
from app.core.security import create_access_token, create_refresh_token, decode_token

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    body: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Register a new user account."""
    try:
        user = await auth_service.register(
            email=body.email,
            password=body.password,
            full_name=body.full_name,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    return UserResponse.model_validate(user)


@router.post("/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Authenticate with email and password, receive JWT tokens."""
    try:
        return await auth_service.login(email=body.email, password=body.password)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))


@router.post("/refresh", response_model=TokenResponse)
async def refresh(body: RefreshRequest):
    """Exchange a valid refresh token for a new access/refresh token pair."""
    try:
        payload = decode_token(body.refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
        subject = payload["sub"]
        return TokenResponse(
            access_token=create_access_token(subject),
            refresh_token=create_refresh_token(subject),
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")
