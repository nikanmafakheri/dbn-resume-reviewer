"""Unit tests for the strict score parser."""

import json

import pytest

from app.ai.parsers.score_parser import ScoreParseError, parse_score_response
from app.core.scoring import weighted_overall


def _valid_payload(overrides: dict | None = None) -> dict:
    """A fully-valid dimension payload (all scores 70, all justified)."""
    payload = {
        "dimensions": {
            name: {
                "score": 70,
                "justification": "A substantive justification that is clearly long enough.",
            }
            for name in ("ats", "skills", "experience", "formatting", "content")
        },
        "strengths": ["Clean structure"],
        "weaknesses": ["Few metrics"],
        "missing_skills": ["Kubernetes"],
        "actionable_recommendations": ["Add quantified impact to 2023 role"],
        "summary_en": "Solid mid-level engineer.",
        "analysis_fa": (
            "این رزومه به‌طور کلی ساختار مناسبی دارد و مهارت‌های فنی اصلی "
            "به‌خوبی مشخص شده‌اند."
        ),
    }
    if overrides:
        payload.update(overrides)
    return payload


class TestScoreParser:
    def test_parse_valid_response(self):
        result = parse_score_response(json.dumps(_valid_payload()))
        assert set(result.dimensions) == {"ats", "skills", "experience", "formatting", "content"}
        assert all(d.score == 70 for d in result.dimensions.values())
        assert result.overall == 70.0
        assert result.confidence.label == "high"
        assert result.strengths == ["Clean structure"]
        assert result.summary == "Solid mid-level engineer."
        assert result.summary_en == "Solid mid-level engineer."
        assert result.analysis_fa.startswith("این رزومه")

    def test_overall_is_weighted_mean_not_llm_value(self):
        payload = _valid_payload({"overall": 5})  # LLM trying to supply its own overall
        result = parse_score_response(json.dumps(payload))
        assert result.overall == 70.0  # computed, not the LLM's 5

    def test_parse_with_feedback_lists(self):
        result = parse_score_response(json.dumps(_valid_payload()))
        assert result.missing_skills == ["Kubernetes"]
        assert result.actionable_recommendations == ["Add quantified impact to 2023 role"]
        assert result.weaknesses == ["Few metrics"]

    def test_weighted_overall_matches_formula(self):
        scores = {"ats": 90, "skills": 80, "experience": 60, "formatting": 100, "content": 50}
        payload = _valid_payload(
            {
                "dimensions": {
                    name: {"score": s, "justification": "A substantive justification that is long."}
                    for name, s in scores.items()
                }
            }
        )
        result = parse_score_response(json.dumps(payload))
        expected = round(0.25 * 90 + 0.25 * 80 + 0.25 * 60 + 0.10 * 100 + 0.15 * 50, 2)
        assert result.overall == expected == weighted_overall(scores)

    def test_parse_invalid_json_raises(self):
        with pytest.raises(ScoreParseError):
            parse_score_response("not json at all")

    def test_parse_empty_response_raises(self):
        with pytest.raises(ScoreParseError):
            parse_score_response("")

    def test_parse_missing_dimension_raises(self):
        payload = _valid_payload()
        del payload["dimensions"]["skills"]
        with pytest.raises(ScoreParseError, match="skills"):
            parse_score_response(json.dumps(payload))

    def test_parse_out_of_range_score_raises(self):
        payload = _valid_payload()
        payload["dimensions"]["ats"]["score"] = 120
        with pytest.raises(ScoreParseError, match="out of range"):
            parse_score_response(json.dumps(payload))

    def test_parse_short_justification_raises(self):
        payload = _valid_payload()
        payload["dimensions"]["ats"]["justification"] = "too short"
        with pytest.raises(ScoreParseError, match="justification"):
            parse_score_response(json.dumps(payload))

    def test_parse_empty_justification_raises(self):
        payload = _valid_payload()
        payload["dimensions"]["ats"]["justification"] = ""
        with pytest.raises(ScoreParseError, match="justification"):
            parse_score_response(json.dumps(payload))

    def test_parse_provider_raw_fallback_raises(self):
        with pytest.raises(ScoreParseError):
            parse_score_response({"raw": "some unparsed text"})

    def test_parse_non_object_rejects(self):
        with pytest.raises(ScoreParseError):
            parse_score_response("[1, 2, 3]")

    def test_markdown_fenced_json_is_accepted(self):
        raw = f"```json\n{json.dumps(_valid_payload())}\n```"
        result = parse_score_response(raw)
        assert result.overall == 70.0

    def test_confidence_drops_when_justifications_thin(self):
        # Conforming (>= 10 chars) but thin (< 40 chars) justifications still
        # validate, yet confidence drops below "high".
        payload = _valid_payload()
        thin = "Thin but conforming."
        payload["dimensions"]["ats"]["justification"] = thin
        payload["dimensions"]["skills"]["justification"] = thin
        payload["dimensions"]["experience"]["justification"] = thin
        result = parse_score_response(json.dumps(payload))
        assert result.confidence.label != "high"
        assert result.confidence.justifications_valid == 2
