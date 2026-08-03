"""Resume upload, listing, deletion, and analysis trigger."""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.core.constants import AnalysisStatus
from app.dependencies import get_analysis_service, get_resume_service
from app.schemas.analysis import AnalysisResponse
from app.schemas.resume import ResumeResponse
from app.services.analysis_service import AnalysisService
from app.services.resume_service import ResumeService
from app.utils.file import is_allowed_file, is_valid_file_size
from app.utils.pdf import extract_text_from_pdf

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/upload", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    resume_service: ResumeService = Depends(get_resume_service),
):
    """Upload a resume file (PDF, DOC, DOCX)."""
    filename = file.filename or "untitled"
    if not is_allowed_file(filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File type not allowed. Allowed: .pdf, .docx",
        )

    content = await file.read()
    if not is_valid_file_size(len(content)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File too large. Maximum size is 10 MB.",
        )

    resume = await resume_service.upload(filename, content)

    # Attempt text extraction from PDF
    if resume.file_path and resume.file_path.lower().endswith(".pdf"):
        try:
            text = extract_text_from_pdf(resume.file_path)
            resume.text_content = text
            await resume_service.resume_repo.save(resume)
        except Exception as exc:
            # Extraction failure shouldn't block upload, but it MUST be visible:
            # an analysis on a text-less resume would otherwise fail mysteriously.
            logger.warning("PDF text extraction failed for %s: %s", filename, exc)

    return ResumeResponse.model_validate(resume)


@router.get("", response_model=list[ResumeResponse])
async def list_resumes(
    resume_service: ResumeService = Depends(get_resume_service),
):
    """List all uploaded resumes."""
    resumes = await resume_service.resume_repo.list_all()
    return [ResumeResponse.model_validate(r) for r in resumes]


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: UUID,
    resume_service: ResumeService = Depends(get_resume_service),
):
    """Delete a resume by ID."""
    resume = await resume_service.resume_repo.get(resume_id)
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await resume_service.resume_repo.delete(resume)


@router.post(
    "/{resume_id}/analyze",
    response_model=AnalysisResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def analyze_resume(
    resume_id: UUID,
    resume_service: ResumeService = Depends(get_resume_service),
    analysis_service: AnalysisService = Depends(get_analysis_service),
):
    """Trigger a new analysis for a resume.

    In the MVP the scoring runs inline (Celery dispatch is unreliable without
    Redis running). Failures are recorded on the Analysis row — never swallowed —
    so the frontend can surface a `failed` status instead of polling forever.
    """
    resume = await resume_service.resume_repo.get(resume_id)
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    analysis = await analysis_service.create_analysis(resume_id=resume.id)

    if resume.text_content:
        from app.dependencies import create_scorer  # patched in tests
        scorer = create_scorer()
        try:
            result = await scorer.score(resume.text_content)
            AnalysisService._apply_result(analysis, result)
            analysis.status = AnalysisStatus.COMPLETED
        except Exception as exc:
            logger.exception("Analysis %s failed for resume %s", analysis.id, resume_id)
            analysis.status = AnalysisStatus.FAILED
            analysis.error_message = str(exc)
    else:
        analysis.status = AnalysisStatus.FAILED
        analysis.error_message = "No extractable text in resume (is it a scanned PDF?)"

    return AnalysisResponse.model_validate(analysis)
