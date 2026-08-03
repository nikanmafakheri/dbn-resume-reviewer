"""Strict parser for LLM scoring responses.

The scoring pipeline is deterministic and explainable:

- The LLM returns the five dimension scores with per-dimension justification,
  plus strengths/weaknesses/missing skills/recommendations/summary.
- The **overall score is never read from the LLM** — it is recomputed here
  (and in the scorer) from the dimension scores using the documented weighted
  formula in ``app/core/scoring.py``.
- Any malformed response (missing dimension, out-of-range score, non-JSON,
  unterminated) is rejected with a descriptive ``ScoreParseError`` so the
  caller can retry with corrective feedback. We never silently clamp or fill
  gaps — a fabricated dimension would corrupt the weighted overall.

Confidence is a structural measure: how much of the requested schema survived
validation. A response missing a justification is structurally weaker and the
parser reflects that in ``Confidence``.
"""

from __future__ import annotations

import json
import logging
import math

from app.core.scoring import (
    CONFIDENCE_HIGH_THRESHOLD,
    CONFIDENCE_LOW_THRESHOLD,
    DIMENSIONS,
    MIN_JUSTIFIED_DIMENSIONS,
    weighted_overall,
)
from app.schemas.analysis import Confidence, DimensionScore, ScoreResult

logger = logging.getLogger(__name__)

SCORE_MIN = 0.0
SCORE_MAX = 100.0
#: Hard floor — a justification shorter than this is empty/garbage and rejects.
_MIN_JUSTIFICATION_LEN = 10
#: Substantive justification — at least this length counts as "valid" for
#: confidence. Justifications that pass validation but stay below this are
#: technically conforming yet thin, so confidence drops below "high".
_QUALITY_JUSTIFICATION_LEN = 40


class ScoreParseError(ValueError):
    """Raised when an LLM response cannot be turned into a valid ScoreResult.

    ``message`` is human-readable and safe to pass back into a retry prompt.
    """

    def __init__(self, message: str, *, retryable: bool = True):
        super().__init__(message)
        self.retryable = retryable


def _ensure_json(raw: str | dict) -> dict:
    """Coerce raw input to a dict, rejecting unparseable payloads."""
    if isinstance(raw, dict):
        data = raw
    elif isinstance(raw, str):
        text = raw.strip()
        # Strip markdown fences if a provider wrapped JSON in them.
        if text.startswith("```"):
            text = text.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
        if not text:
            raise ScoreParseError("LLM returned an empty response")
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ScoreParseError(
                f"LLM response was not valid JSON: {exc.msg} at position {exc.pos}"
            ) from exc
        if not isinstance(data, dict):
            raise ScoreParseError("LLM JSON response was not an object")
    else:
        raise ScoreParseError(f"Unexpected response type from provider: {type(raw).__name__}")
    return data


def _parse_float(value, what: str) -> float:
    """Coerce a value to a finite number or raise a descriptive error."""
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ScoreParseError(f"`{what}` must be a number, got: {value!r}") from exc
    if not math.isfinite(number):
        raise ScoreParseError(f"`{what}` must be a finite number, got: {value!r}")
    return number


def _parse_dimension(name: str, raw) -> DimensionScore:
    """Parse and validate one dimension object with a justification."""
    if not isinstance(raw, dict):
        raise ScoreParseError(f"`dimensions.{name}` must be an object with score and justification")

    score = _parse_float(raw.get("score"), f"dimensions.{name}.score")
    if score < SCORE_MIN or score > SCORE_MAX:
        raise ScoreParseError(f"`dimensions.{name}.score` out of range 0-100: {score}")

    justification = raw.get("justification", "")
    if not isinstance(justification, str):
        raise ScoreParseError(f"`dimensions.{name}.justification` must be a string")
    justification = justification.strip()
    if len(justification) < _MIN_JUSTIFICATION_LEN:
        raise ScoreParseError(
            f"`dimensions.{name}.justification` must be at least {_MIN_JUSTIFICATION_LEN} "
            "characters explaining the score"
        )

    return DimensionScore(score=score, justification=justification)


def _parse_string_list(raw, what: str) -> list[str]:
    if not isinstance(raw, list):
        raise ScoreParseError(f"`{what}` must be a list of strings")
    out: list[str] = []
    for item in raw:
        if not isinstance(item, str) or not item.strip():
            raise ScoreParseError(f"`{what}` must contain only non-empty strings")
        out.append(item.strip())
    return out


def parse_score_response(raw: str | dict) -> ScoreResult:
    """Parse and strictly validate an LLM scoring response.

    Args:
        raw: Raw JSON string or already-parsed dict from a provider.

    Returns:
        A validated ``ScoreResult`` whose ``overall`` was computed
        deterministically from the dimension scores.

    Raises:
        ScoreParseError: On any malformed/missing/out-of-range field. The
            message is suitable for a retry prompt.
    """
    data = _ensure_json(raw)
    if not isinstance(data, dict):
        raise ScoreParseError("LLM JSON response must be an object")

    # Providers fall back to {"raw": <text>} when JSON parsing fails — a hard
    # parse failure, not a score payload.
    if "raw" in data and "dimensions" not in data:
        raise ScoreParseError("LLM returned an unparsed JSON response")

    dims_raw = data.get("dimensions")
    if not isinstance(dims_raw, dict):
        raise ScoreParseError("`dimensions` is missing or not an object")

    dimensions: dict[str, DimensionScore] = {}
    missing: list[str] = []
    for name in DIMENSIONS:
        if name not in dims_raw:
            missing.append(name)
            continue
        dimensions[name] = _parse_dimension(name, dims_raw[name])

    if missing:
        raise ScoreParseError(f"Missing required dimension(s): {', '.join(missing)}")

    justified = sum(
        1
        for dim in dimensions.values()
        if len(dim.justification.strip()) >= _QUALITY_JUSTIFICATION_LEN
    )
    confidence_score = round(justified / len(DIMENSIONS), 2)
    if confidence_score >= CONFIDENCE_HIGH_THRESHOLD:
        label = "high"
    elif confidence_score >= CONFIDENCE_LOW_THRESHOLD:
        label = "medium"
    else:
        label = "low"

    confidence = Confidence(
        label=label,
        score=confidence_score,
        justifications_valid=justified,
        note=(
            "All dimension scores justified"
            if justified == MIN_JUSTIFIED_DIMENSIONS
            else f"{justified}/{MIN_JUSTIFIED_DIMENSIONS} dimensions justified"
        ),
    )

    overall = weighted_overall({name: dim.score for name, dim in dimensions.items()})

    return ScoreResult(
        dimensions=dimensions,
        overall=overall,
        confidence=confidence,
        strengths=_parse_string_list(data.get("strengths", []), "strengths"),
        weaknesses=_parse_string_list(data.get("weaknesses", []), "weaknesses"),
        missing_skills=_parse_string_list(data.get("missing_skills", []), "missing_skills"),
        actionable_recommendations=_parse_string_list(
            data.get("actionable_recommendations", []), "actionable_recommendations"
        ),
        summary=str(data.get("summary_en", "")).strip(),
        summary_en=str(data.get("summary_en", "")).strip(),
        analysis_fa=str(data.get("analysis_fa", "")).strip(),
    )
