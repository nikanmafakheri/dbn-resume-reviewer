"""Unit tests for the ResumeScorer retry + deterministic-formula pipeline."""


import pytest

from app.ai.parsers.score_parser import ScoreParseError
from app.ai.scorers.resume_scorer import MAX_RETRIES, ResumeScorer


def _valid_payload() -> dict:
    return {
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
        "analysis_fa": "این رزومه ساختار منظمی دارد و مهارت‌های اصلی به‌خوبی مشخص شده‌اند.",
    }


class _FakeProvider:
    """Provider that returns a scripted sequence of responses."""

    def __init__(self, responses: list):
        self.responses = list(responses)
        self.prompts: list[str] = []

    async def generate(self, prompt: str, schema=None):
        self.prompts.append(prompt)
        return self.responses.pop(0) if self.responses else {"raw": "exhausted"}


@pytest.mark.asyncio
class TestResumeScorer:
    async def test_valid_response_succeeds_on_first_pass(self):
        provider = _FakeProvider([_valid_payload()])
        result = await ResumeScorer(provider).score("...resume...")
        assert result.overall == 70.0
        assert len(provider.prompts) == 1

    async def test_malformed_response_is_retried_with_corrective_prompt(self):
        # First pass: missing dimension → rejected. Second pass: valid.
        bad = _valid_payload()
        del bad["dimensions"]["skills"]
        provider = _FakeProvider([bad, _valid_payload()])
        result = await ResumeScorer(provider).score("...resume...")
        assert result.overall == 70.0
        assert len(provider.prompts) == 2
        # The retry prompt embeds the corrective validation error and the schema reminder.
        assert "validation is missing" not in provider.prompts[1]
        assert "ScoreParse" in provider.prompts[1] or "dimension" in provider.prompts[1]

    async def test_persistent_malformed_response_raises_after_retries(self):
        bad = {"dimensions": {"ats": {"score": 200, "justification": "short"}}}
        provider = _FakeProvider([bad, bad, bad])
        scorer = ResumeScorer(provider)
        with pytest.raises(ScoreParseError):
            await scorer.score("...resume...")
        assert len(provider.prompts) == MAX_RETRIES + 1

    async def test_non_json_provider_fallback_raises(self):
        provider = _FakeProvider([{"raw": "not json"}])
        with pytest.raises(ScoreParseError):
            await ResumeScorer(provider).score("...resume...")
