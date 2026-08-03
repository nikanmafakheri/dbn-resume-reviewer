"""Orchestrates resume scoring using LLM providers and parsers.

Guarantees of this pipeline:

- The **overall score is deterministic**: computed by the parser from the five
  dimension scores via the documented weighted formula — the LLM never supplies
  an arbitrary overall value.
- **Malformed responses are rejected and retried**: if the LLM returns
  non-JSON, a missing/out-of-range dimension, or an unjustified score, the
  scorer re-prompts once with the exact parse error as corrective feedback.
  After exhausting retries the failure is surfaced to the caller.
- **Every score is justified**: the parser enforces a per-dimension
  justification before a result is accepted.
"""

from __future__ import annotations

import logging
from pathlib import Path

from app.ai.parsers.score_parser import ScoreParseError, parse_score_response
from app.ai.providers.base import BaseLLMProvider
from app.core.scoring import DIMENSION_WEIGHTS, DIMENSIONS, weighted_overall
from app.schemas.analysis import ScoreResult

logger = logging.getLogger(__name__)

#: How many times to re-prompt the LLM after a malformed/unjustified response.
MAX_RETRIES = 2


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

    async def _generate(self, prompt: str) -> dict:
        return await self.provider.generate(prompt, schema=ScoreResult)

    async def score(self, resume_text: str) -> ScoreResult:
        """Run the evaluation pipeline: prompt → validate → retry on failure.

        Returns a validated ``ScoreResult`` whose ``overall`` was derived from
        the dimension scores. Raises the last ``ScoreParseError`` if the LLM
        cannot produce a conforming response after ``MAX_RETRIES`` attempts.
        """
        prompt = _load_prompt("resume_analysis.md", resume_text=resume_text)
        raw = await self._generate(prompt)

        for attempt in range(MAX_RETRIES + 1):
            try:
                result = parse_score_response(raw)
                self._verify_overall(result)
                return result
            except ScoreParseError as exc:
                logger.warning(
                    "Score parse failed (attempt %d/%d): %s", attempt + 1, MAX_RETRIES + 1, exc
                )
                if attempt == MAX_RETRIES:
                    raise
                prompt = self._build_retry_prompt(resume_text, str(exc))
                raw = await self._generate(prompt)

        raise RuntimeError("Unexpected end of scoring loop")  # pragma: no cover

    @staticmethod
    def _verify_overall(result: ScoreResult) -> None:
        """Guard against parser/formula drift — recompute and compare.

        The parser already computes ``overall`` deterministically; this is a
        cheap internal consistency check that catches a regression where the
        stored overall diverges from the weighted formula.
        """
        expected = weighted_overall({name: dim.score for name, dim in result.dimensions.items()})
        if abs(expected - result.overall) > 1e-6:
            raise ScoreParseError(
                "Internal inconsistency: overall score does not match the weighted formula"
            )

    def _build_retry_prompt(self, resume_text: str, error: str) -> str:
        """Construct a corrective prompt embedding the exact parse error.

        The original evaluation instructions are re-included so the retry is
        self-contained, plus the JSON schema reminder and the specific failure
        the model must fix.
        """
        base = _load_prompt("resume_analysis.md", resume_text=resume_text)
        return (
            f"{base}\n\n"
            "# Corrective feedback — the previous response was rejected.\n"
            "Return only the required JSON object. Nothing else, no markdown fences.\n"
            f"Validation error: {error}\n"
            "Fix the response so it satisfies the schema exactly and retry."
        )

    # ── Schema hint surfaced to prompts / diagnostics ──────────────────────
    @staticmethod
    def schema_hint() -> str:
        """Human-readable description of the required JSON contract."""
        weights = ", ".join(f"{name} {int(DIMENSION_WEIGHTS[name] * 100)}%" for name in DIMENSIONS)
        return f"Dimensions ({weights}): ATS, Skills, Experience, Formatting, Content Quality."
