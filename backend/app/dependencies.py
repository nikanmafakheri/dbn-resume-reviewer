"""Global dependency injection."""

from fastapi import Depends

from app.core.database import get_db
from app.repositories.resume_repo import ResumeRepository
from app.repositories.analysis_repo import AnalysisRepository
from app.repositories.dbn_standard_repo import DBNStandardRepository
from app.services.resume_service import ResumeService
from app.services.analysis_service import AnalysisService
from app.services.scoring_service import ScoringService
from app.services.dbn_standard_service import DBNStandardService
from app.ai.scorers.resume_scorer import ResumeScorer
from app.core.config import settings


# ── Repositories ──
def get_resume_repo(db=Depends(get_db)) -> ResumeRepository:
    return ResumeRepository(db)


def get_analysis_repo(db=Depends(get_db)) -> AnalysisRepository:
    return AnalysisRepository(db)


def get_standard_repo(db=Depends(get_db)) -> DBNStandardRepository:
    return DBNStandardRepository(db)


# ── AI ──
def get_llm_provider():
    if settings.LLM_PROVIDER == "gemini":
        from app.ai.providers.gemini import GeminiProvider
        return GeminiProvider()
    elif settings.LLM_PROVIDER == "openai":
        from app.ai.providers.openai import OpenAIProvider
        return OpenAIProvider()
    elif settings.LLM_PROVIDER == "claude":
        from app.ai.providers.claude import ClaudeProvider
        return ClaudeProvider()
    else:
        from app.ai.providers.openrouter import OpenRouterProvider
        return OpenRouterProvider()


def create_scorer() -> ResumeScorer:
    """Standalone factory for ResumeScorer (usable outside FastAPI DI, e.g. Celery)."""
    if settings.LLM_PROVIDER == "gemini":
        from app.ai.providers.gemini import GeminiProvider
        provider = GeminiProvider()
    elif settings.LLM_PROVIDER == "openai":
        from app.ai.providers.openai import OpenAIProvider
        provider = OpenAIProvider()
    elif settings.LLM_PROVIDER == "claude":
        from app.ai.providers.claude import ClaudeProvider
        provider = ClaudeProvider()
    else:
        from app.ai.providers.openrouter import OpenRouterProvider
        provider = OpenRouterProvider()
    return ResumeScorer(provider)


def get_scorer(provider=Depends(get_llm_provider)) -> ResumeScorer:
    return ResumeScorer(provider)


# ── Services ──
def get_resume_service(repo: ResumeRepository = Depends(get_resume_repo)) -> ResumeService:
    return ResumeService(repo)


def get_analysis_service(
    repo: AnalysisRepository = Depends(get_analysis_repo),
    scorer: ResumeScorer = Depends(get_scorer),
) -> AnalysisService:
    return AnalysisService(repo, scorer)


def get_scoring_service(repo: DBNStandardRepository = Depends(get_standard_repo)) -> ScoringService:
    return ScoringService(repo)


def get_standard_service(repo: DBNStandardRepository = Depends(get_standard_repo)) -> DBNStandardService:
    return DBNStandardService(repo)
