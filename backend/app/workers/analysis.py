"""Resume analysis Celery task."""

import logging
from app.workers.celery import celery_app
from app.domain.models.analysis import Analysis
from app.core.constants import AnalysisStatus

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def analyze_resume(self, analysis_id: str):
    """Run full resume analysis in the background.

    1. Load analysis + resume from DB
    2. Extract text from resume file
    3. Call LLM via ResumeScorer
    4. Persist scores
    """
    logger.info("Starting analysis %s", analysis_id)
    # Implementation in subsequent iteration
