"""Orchestrates resume scoring using LLM providers and parsers."""

import logging
from pathlib import Path

from app.ai.providers.base import BaseLLMProvider
from app.ai.parsers.score_parser import parse_score_response
from app.core.config import settings
from app.schemas.analysis import ScoreResult

logger = logging.getLogger(__name__)


def _load_prompt(name: str, **kwargs) -> str:
    path = Path(__file__).parent.parent / "prompts" / name
    return path.read_text().format(**kwargs)


class ResumeScorer:
    def __init__(self, provider: BaseLLMProvider):
        self.provider = provider

    async def score(self, resume_text: str) -> ScoreResult:
        prompt = _load_prompt("resume_analysis.md", resume_text=resume_text)
        raw = await self.provider.generate(prompt)
        return parse_score_response(raw)
