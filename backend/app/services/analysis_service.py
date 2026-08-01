"""Analysis service — orchestrates the analysis workflow."""

from uuid import UUID

from app.ai.scorers.resume_scorer import ResumeScorer
from app.core.constants import AnalysisStatus
from app.core.database import Database
from app.domain.models.analysis import Analysis
from app.repositories.analysis_repo import AnalysisRepository


class AnalysisService:
    def __init__(self, analysis_repo: AnalysisRepository, scorer: ResumeScorer):
        self.analysis_repo = analysis_repo
        self.scorer = scorer

    async def create_analysis(self, resume_id: UUID) -> Analysis:
        analysis = Analysis(
            resume_id=resume_id,
            user_id=UUID(Database.ANONYMOUS_USER_ID),
            status=AnalysisStatus.PENDING,
        )
        return await self.analysis_repo.save(analysis)

    async def run_analysis(self, analysis_id: str, resume_text: str):
        """Called from Celery worker."""
        analysis = await self.analysis_repo.get(analysis_id)
        if not analysis:
            return

        analysis.status = AnalysisStatus.PROCESSING
        try:
            result = await self.scorer.score(resume_text)
            analysis.overall_score = result.overall_score
            analysis.ats_score = result.ats_score
            analysis.grammar_score = result.grammar_score
            analysis.recruiter_score = result.recruiter_score
            analysis.summary = result.summary
            analysis.feedback_json = result.feedback or None
            analysis.status = AnalysisStatus.COMPLETED
        except Exception as exc:
            analysis.status = AnalysisStatus.FAILED
            analysis.error_message = str(exc)
