"""DBN Standard (scoring rubric) routes."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_current_user, get_standard_service, get_scoring_service
from app.domain.models.user import User
from app.services.dbn_standard_service import DBNStandardService
from app.services.scoring_service import ScoringService
from app.schemas.dbn_standard import StandardCreate, StandardResponse

router = APIRouter()


@router.get("", response_model=StandardResponse)
async def get_active_standard(
    scoring_service: ScoringService = Depends(get_scoring_service),
):
    """Return the currently active DBN scoring standard."""
    standard = await scoring_service.get_active_standard()
    if not standard:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active standard")
    return StandardResponse.model_validate(standard)


@router.post("", response_model=StandardResponse, status_code=status.HTTP_201_CREATED)
async def create_standard(
    body: StandardCreate,
    current_user: User = Depends(get_current_user),
    standard_service: DBNStandardService = Depends(get_standard_service),
):
    """Create a new DBN scoring standard."""
    standard = await standard_service.create_standard(
        name=body.name,
        version=body.version,
        description=body.description,
        created_by=str(current_user.id),
    )
    return StandardResponse.model_validate(standard)
