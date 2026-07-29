"""Analysis retrieval routes."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_analysis_service
from app.services.analysis_service import AnalysisService
from app.schemas.analysis import AnalysisResponse

router = APIRouter()


@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(
    analysis_id: str,
    analysis_service: AnalysisService = Depends(get_analysis_service),
):
    """Get the analysis results for a given analysis ID."""
    analysis = await analysis_service.analysis_repo.get(UUID(analysis_id))
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return AnalysisResponse.model_validate(analysis)
