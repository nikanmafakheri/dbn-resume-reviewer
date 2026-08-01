"""Parse structured LLM responses into score dicts.

The LLM providers return the *parsed* payload (a ``dict`` from ``json.loads``)
or, as a last-resort fallback, ``{"raw": "<unparsed text>"}``. This parser
accepts both shapes so the provider->parser contract is stable regardless of
which provider is configured.
"""

import json
import logging

from pydantic import ValidationError

from app.schemas.analysis import ScoreResult

logger = logging.getLogger(__name__)


def _clamp_score(value, lo: float = 0.0, hi: float = 100.0) -> float:
    """Coerce a raw score value to a valid 0-100 float."""
    try:
        return max(lo, min(hi, float(value)))
    except (TypeError, ValueError):
        return 0.0


def parse_score_response(raw: str | dict) -> ScoreResult:
    """Parse LLM output into a validated, clamped ScoreResult.

    Args:
        raw: Either a JSON string or an already-parsed dict.

    Returns:
        ScoreResult with all scores clamped to 0-100.

    Raises:
        json.JSONDecodeError: If ``raw`` is a string that is not valid JSON.
        ValidationError: If required score fields are missing/not coercible.
    """
    if isinstance(raw, str):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            logger.error("LLM response was not valid JSON: %.200s", raw)
            raise
    elif isinstance(raw, dict):
        data = raw
    else:
        raise ValidationError.from_exception_data(
            "ScoreResult",
            [{"type": "string_type", "loc": ("raw",), "input": raw}],
        )

    # Providers fall back to {"raw": <text>} when JSON parsing fails — that is
    # a hard parse failure, not a score payload.
    if "raw" in data and not any(k.startswith("score") for k in data):
        raise ValidationError.from_exception_data(
            "ScoreResult",
            [{"type": "missing", "loc": ("scores",), "input": data}],
        )

    try:
        return ScoreResult(
            overall_score=_clamp_score(data["overall_score"]),
            ats_score=_clamp_score(data["ats_score"]),
            grammar_score=_clamp_score(data["grammar_score"]),
            recruiter_score=_clamp_score(data["recruiter_score"]),
            summary=str(data.get("summary", "")),
            feedback=data.get("feedback") or {},
        )
    except (KeyError, TypeError) as exc:
        logger.error("LLM score payload missing required fields: %s", exc)
        raise ValidationError.from_exception_data(
            "ScoreResult",
            [{"type": "missing", "loc": ("scores",), "input": data}],
        ) from exc
