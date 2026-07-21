"""Parse structured LLM responses into score dicts."""

import json
import logging
from pydantic import ValidationError
from app.schemas.analysis import ScoreResult

logger = logging.getLogger(__name__)


def parse_score_response(raw: str) -> ScoreResult:
    """Parse LLM JSON output into a validated ScoreResult."""
    try:
        data = json.loads(raw)
        return ScoreResult(**data)
    except (json.JSONDecodeError, ValidationError) as exc:
        logger.error("Failed to parse LLM response: %s", exc)
        raise
