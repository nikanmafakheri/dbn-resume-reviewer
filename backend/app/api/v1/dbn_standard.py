"""DBN Standard (scoring rubric) routes."""

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse

from app.core.config import settings
from app.dependencies import get_scoring_service, get_standard_service
from app.schemas.dbn_standard import StandardCreate, StandardResponse
from app.services.dbn_standard_service import DBNStandardService
from app.services.scoring_service import ScoringService

router = APIRouter()


# ── Template download ──────────────────────────────────────────────
# Serves the DBN Standard resume template file (.pptx) that users download
# from the landing page. The file lives in the repo at
# `dbn-standard-resume-template/` and is resolved via settings.TEMPLATE_PPTX_PATH.
@router.get("/template/download")
async def download_template() -> FileResponse:
    """Download the DBN Standard resume template as a .pptx file."""
    template_path: Path = settings.TEMPLATE_PPTX_PATH
    if not template_path.exists() or not template_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template file not found.",
        )
    return FileResponse(
        template_path,
        media_type=(
            "application/vnd.openxmlformats-officedocument."
            "presentationml.presentation"
        ),
        filename="dbn-standard-resume-template.pptx",
    )


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
    standard_service: DBNStandardService = Depends(get_standard_service),
):
    """Create a new DBN scoring standard."""
    standard = await standard_service.create_standard(
        name=body.name,
        version=body.version,
        description=body.description,
    )
    return StandardResponse.model_validate(standard)
