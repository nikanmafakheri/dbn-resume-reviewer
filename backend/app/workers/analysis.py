"""Resume analysis Celery task — runs LLM scoring in the background."""

import asyncio
import logging

from app.workers.celery import celery_app
from app.core.database import init_database, get_database
from app.core.constants import AnalysisStatus
from app.dependencies import create_scorer

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def analyze_resume(self, analysis_id: str):
    """Run full resume analysis in the background.

    1. Load analysis + resume from DB
    2. Extract text from resume file (if not already extracted)
    3. Call LLM via ResumeScorer
    4. Persist scores
    """
    logger.info("Starting analysis %s", analysis_id)
    try:
        asyncio.run(_run_analysis(analysis_id))
    except Exception as exc:
        logger.exception("Analysis %s failed with unhandled error: %s", analysis_id, exc)
        raise self.retry(exc=exc)


async def _run_analysis(analysis_id: str):
    """Async implementation of the resume analysis pipeline."""
    init_database()
    db = get_database()

    async with db.session_factory() as session:
        from app.repositories.analysis_repo import AnalysisRepository
        from app.repositories.resume_repo import ResumeRepository
        from app.services.analysis_service import AnalysisService
        from app.utils.pdf import extract_text_from_pdf

        analysis_repo = AnalysisRepository(session)
        resume_repo = ResumeRepository(session)

        # 1. Load analysis record
        analysis = await analysis_repo.get(analysis_id)
        if not analysis:
            logger.error("Analysis %s not found — aborting", analysis_id)
            return

        # 2. Load associated resume
        resume = await resume_repo.get(analysis.resume_id)
        if not resume:
            analysis.status = AnalysisStatus.FAILED
            analysis.error_message = "Associated resume not found"
            await session.flush()
            await session.commit()
            logger.error("Resume for analysis %s not found", analysis_id)
            return

        # 3. Ensure we have text content
        resume_text = resume.text_content
        if not resume_text and resume.file_path:
            logger.info("Extracting text from %s", resume.file_path)
            try:
                resume_text = extract_text_from_pdf(resume.file_path)
                resume.text_content = resume_text
            except Exception as exc:
                logger.error("PDF extraction failed for %s: %s", resume.file_path, exc)
                analysis.status = AnalysisStatus.FAILED
                analysis.error_message = f"PDF extraction failed: {exc}"
                await session.flush()
                await session.commit()
                return

        if not resume_text:
            analysis.status = AnalysisStatus.FAILED
            analysis.error_message = "No text content available for analysis"
            await session.flush()
            await session.commit()
            logger.error("No text content for analysis %s", analysis_id)
            return

        # 4. Run LLM scoring
        logger.info("Running LLM scoring for analysis %s", analysis_id)
        scorer = create_scorer()
        service = AnalysisService(analysis_repo, scorer)
        await service.run_analysis(analysis_id, resume_text)

        # 5. Commit all changes
        await session.commit()
        logger.info("Analysis %s completed successfully", analysis_id)
