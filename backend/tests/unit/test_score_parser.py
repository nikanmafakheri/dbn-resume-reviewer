"""Unit tests for the score parser."""

import json

import pytest
from pydantic import ValidationError

from app.ai.parsers.score_parser import parse_score_response
from app.schemas.analysis import ScoreResult


class TestScoreParser:
    def test_parse_valid_response(self):
        raw = (
            '{"overall_score": 85, "ats_score": 70, "grammar_score": 90, '
            '"recruiter_score": 80, "summary": "Good resume"}'
        )
        result = parse_score_response(raw)
        assert isinstance(result, ScoreResult)
        assert result.overall_score == 85
        assert result.ats_score == 70
        assert result.grammar_score == 90
        assert result.recruiter_score == 80
        assert result.summary == "Good resume"

    def test_parse_with_feedback(self):
        raw = (
            '{"overall_score": 75, "ats_score": 65, "grammar_score": 80, "recruiter_score": 70, '
            '"summary": "Decent", "feedback": {"strengths": ["Clear format"]}}'
        )
        result = parse_score_response(raw)
        assert result.feedback == {"strengths": ["Clear format"]}

    def test_parse_invalid_json_raises(self):
        with pytest.raises((ValidationError, json.JSONDecodeError)):
            parse_score_response("not json at all")

    def test_parse_missing_fields_raises(self):
        with pytest.raises(ValidationError):
            parse_score_response('{"overall_score": 85}')
