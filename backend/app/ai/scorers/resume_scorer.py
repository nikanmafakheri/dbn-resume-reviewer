"""Orchestrates resume scoring using LLM providers and parsers."""

import logging
from pathlib import Path

from app.ai.parsers.score_parser import parse_score_response
from app.ai.providers.base import BaseLLMProvider
from app.schemas.analysis import ScoreResult

logger = logging.getLogger(__name__)


def _load_prompt(name: str, **kwargs) -> str:
    """Load a prompt template from the prompts directory.

    Uses plain string replacement rather than ``str.format`` so resume text
    containing ``{`` / ``}`` (very common in code samples) never crashes the
    template render.
    """
    path = Path(__file__).parent.parent / "prompts" / name
    text = path.read_text(encoding="utf-8")
    for key, value in kwargs.items():
        text = text.replace("{" + key + "}", str(value))
    return text


class ResumeScorer:
    def __init__(self, provider: BaseLLMProvider):
        self.provider = provider

    async def score(self, resume_text: str) -> ScoreResult:
        """Run a single LLM pass scoring the resume across all four dimensions."""
        prompt = _load_prompt("resume_analysis.md", resume_text=resume_text)
        raw = await self.provider.generate(prompt, schema=ScoreResult)
        return parse_score_response(raw)
