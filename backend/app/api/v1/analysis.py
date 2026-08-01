"""Analysis retrieval routes."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_analysis_service
from app.schemas.analysis import AnalysisResponse
from app.services.analysis_service import AnalysisService

router = APIRouter()


@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(
    analysis_id: UUID,
    analysis_service: AnalysisService = Depends(get_analysis_service),
):
    """Get the analysis results for a given analysis ID.

    The path param is declared as ``UUID`` so FastAPI validates it and returns
    a 422 on a malformed value instead of a raw 500.
    """
    analysis = await analysis_service.analysis_repo.get(analysis_id)
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return AnalysisResponse.model_validate(analysis)
