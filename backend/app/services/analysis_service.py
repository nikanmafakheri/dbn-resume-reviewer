"""Analysis service — orchestrates the analysis workflow."""

from uuid import UUID

from app.ai.providers.base import ProviderRateLimitError
from app.ai.scorers.resume_scorer import ResumeScorer
from app.core.constants import AnalysisStatus
from app.core.database import Database
from app.core.scoring import DIMENSIONS
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
            self._apply_result(analysis, result)
            analysis.status = AnalysisStatus.COMPLETED
        except Exception as exc:
            analysis.status = AnalysisStatus.FAILED
            analysis.error_message = str(exc)
            if isinstance(exc, ProviderRateLimitError):
                analysis.error_code = "rate_limited"

    @staticmethod
    def _apply_result(analysis: Analysis, result) -> None:
        """Persist a validated ScoreResult into the Analysis row.

        Mirrors the five dimension scores into dedicated columns for cheap
        filtering and stores the full nested result (dimensions with
        justifications, confidence, strengths/weaknesses/recommendations) in
        ``scores_json``. The overall score is the deterministic weighted mean
        already computed by the parser — never read from the LLM.
        """
        analysis.overall_score = result.overall
        analysis.ats_score = result.dimensions["ats"].score
        for name in DIMENSIONS:
            setattr(analysis, f"{name}_score", result.dimensions[name].score)
        analysis.summary = result.summary
        analysis.summary_en = result.summary_en
        analysis.analysis_fa = result.analysis_fa
        analysis.feedback_json = {
            "strengths": result.strengths,
            "weaknesses": result.weaknesses,
            "missing_skills": result.missing_skills,
            "actionable_recommendations": result.actionable_recommendations,
        }
        analysis.scores_json = result.model_dump()
