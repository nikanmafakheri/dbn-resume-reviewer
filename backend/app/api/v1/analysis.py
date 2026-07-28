"""Analysis retrieval routes."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_current_user, get_analysis_service
from app.domain.models.user import User
from app.services.analysis_service import AnalysisService
from app.schemas.analysis import AnalysisResponse

router = APIRouter()


@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(
    analysis_id: str,
    current_user: User = Depends(get_current_user),
    analysis_service: AnalysisService = Depends(get_analysis_service),
):
    """Get the analysis results for a given analysis ID."""
    analysis = await analysis_service.analysis_repo.get(analysis_id)
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if str(analysis.user_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return AnalysisResponse.model_validate(analysis)
