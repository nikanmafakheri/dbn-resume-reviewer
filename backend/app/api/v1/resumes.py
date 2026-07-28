"""Resume upload, listing, deletion, and analysis trigger."""

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status

from app.dependencies import get_current_user, get_resume_service, get_analysis_service
from app.domain.models.user import User
from app.services.resume_service import ResumeService
from app.services.analysis_service import AnalysisService
from app.schemas.resume import ResumeResponse
from app.schemas.analysis import AnalysisResponse
from app.utils.file import is_allowed_file, is_valid_file_size
from app.utils.pdf import extract_text_from_pdf

router = APIRouter()


@router.post("/upload", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    resume_service: ResumeService = Depends(get_resume_service),
):
    """Upload a resume file (PDF, DOC, DOCX)."""
    filename = file.filename or "untitled"
    if not is_allowed_file(filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed: .pdf, .doc, .docx",
        )

    content = await file.read()
    if not is_valid_file_size(len(content)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File too large. Maximum size is 10 MB.",
        )

    resume = await resume_service.upload(str(current_user.id), filename, content)

    # Attempt text extraction from PDF
    if resume.file_path and resume.file_path.lower().endswith(".pdf"):
        try:
            text = extract_text_from_pdf(resume.file_path)
            resume.text_content = text
            await resume_service.resume_repo.save(resume)
        except Exception:
            pass  # extraction failure shouldn't block upload

    return ResumeResponse.model_validate(resume)


@router.get("", response_model=list[ResumeResponse])
async def list_resumes(
    current_user: User = Depends(get_current_user),
    resume_service: ResumeService = Depends(get_resume_service),
):
    """List all resumes for the authenticated user."""
    resumes = await resume_service.resume_repo.list_by_user(current_user.id)
    return [ResumeResponse.model_validate(r) for r in resumes]


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    resume_service: ResumeService = Depends(get_resume_service),
):
    """Delete a resume by ID (must own the resume)."""
    resume = await resume_service.resume_repo.get(resume_id)
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if str(resume.user_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await resume_service.resume_repo.delete(resume)


@router.post("/{resume_id}/analyze", response_model=AnalysisResponse, status_code=status.HTTP_202_ACCEPTED)
async def analyze_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    resume_service: ResumeService = Depends(get_resume_service),
    analysis_service: AnalysisService = Depends(get_analysis_service),
):
    """Trigger a new analysis for a resume. The analysis runs in the background via Celery."""
    resume = await resume_service.resume_repo.get(resume_id)
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if str(resume.user_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    analysis = await analysis_service.create_analysis(
        resume_id=str(resume.id),
        user_id=str(current_user.id),
    )

    # Dispatch Celery task
    from app.workers.analysis import analyze_resume as analyze_task
    analyze_task.delay(str(analysis.id))

    return AnalysisResponse.model_validate(analysis)
