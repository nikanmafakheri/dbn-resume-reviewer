"""DBN Resume evaluation rubric — the single source of truth for scoring.

Every score an LLM emits is a *judgment of sub-criteria evidence*; the DBN
Overall Score is then derived deterministically from the five component scores
via a documented weighted formula. The AI never invents an overall score.

The rubric, dimension weights, and formula here are shared by:
  - the scoring prompt (`app/ai/prompts/resume_analysis.md`),
  - the strict parser/validator (`app/ai/parsers/score_parser.py`),
  - the deterministic recomputation in `app/ai/scorers/resume_scorer.py`.

Weights sum to exactly 1.0 so ``overall`` is the true weighted mean.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Literal

# ── Score dimensions ────────────────────────────────────────────────────────
#: Canonical order of the five evaluated dimensions.
DIMENSIONS: tuple[str, ...] = ("ats", "skills", "experience", "formatting", "content")

#: Weighted formula for the DBN Overall Score. Weights must sum to 1.0.
DIMENSION_WEIGHTS: dict[str, float] = {
    "ats": 0.25,
    "skills": 0.25,
    "experience": 0.25,
    "formatting": 0.10,
    "content": 0.15,
}

#: Rubric — each dimension explains what is judged and the sub-criteria the LLM
#: uses to reach a defensible score. Kept in prose so the prompt stays readable
#: and the same rationale is re-usable for human review/explainability.
DIMENSION_RUBRIC: dict[str, str] = {
    "ats": (
        "Compatibility with Applicant Tracking Systems. Judge keyword coverage "
        "against the target role and common ATS vocabulary, presence of standard "
        "section headings (contact, summary, skills, experience, education), "
        "machine-readable text (no tables/images/columns), and whether "
        "acronyms/technologies are spelled out for parser matching."
    ),
    "skills": (
        "Depth and relevance of hard and soft skills. Judge whether skills are "
        "explicitly listed, how relevant they are to the target role, evidence "
        "of depth (beyond keyword lists — e.g. tools, frameworks, seniority), "
        "and whether proficiency/level is indicated."
    ),
    "experience": (
        "Quality and impact of work history. Judge role relevance, scope and "
        "seniority, concrete outcomes with metrics where available, "
        "action-oriented language (led, built, reduced, shipped) vs passive "
        "descriptions, recency/relevance of history, and clarity of dates and "
        "companies."
    ),
    "formatting": (
        "Visual and structural layout. Judge readable font and consistent "
        "spacing, standard one-page-or-appropriate length, clear section "
        "hierarchy, no distracting graphics/colors/errors, and clean "
        "machine-parseable layout for ATS extraction."
    ),
    "content": (
        "Overall writing quality and completeness. Judge clarity, concision, "
        "grammar/spelling/punctuation, tailored messaging (summary aligned to "
        "the role), and whether required sections (education, links, "
        "certifications) are present and complete."
    ),
}

# ── Confidence (calibration) ────────────────────────────────────────────────
#: Minimum number of *justified* dimensions required to label a result confident.
MIN_JUSTIFIED_DIMENSIONS = 5

#: Confidence reflects how much of the scoring rationale survived validation
#: (it is a structural gate, not an LLM self-estimate — see scorer).
CONFIDENCE_LOW_THRESHOLD = 0.6
CONFIDENCE_HIGH_THRESHOLD = 0.8

Confidence = Literal["low", "medium", "high"]

#: Overall-score bands used for display coloring and band labels.
BAND_LOW = 50.0
BAND_MID = 75.0


def weighted_overall(scores: dict[str, float]) -> float:
    """Compute the DBN Overall Score as the weighted mean of the dimensions.

    Weights live only in :data:`DIMENSION_WEIGHTS`. Unknown/missing dimensions
    contribute 0 (callers validate presence first) so the result is a stable,
    deterministic function of the five inputs.
    """
    return round(
        sum(DIMENSION_WEIGHTS.get(dim, 0.0) * float(scores.get(dim, 0.0)) for dim in DIMENSIONS),
        2,
    )


def band(value: float) -> str:
    """Map a 0-100 score to a display band key."""
    if value >= BAND_MID:
        return "great" if value >= BAND_MID + (100 - BAND_MID) / 2 else "good"
    return "mid" if value >= BAND_LOW else "low"


# ── Classification helpers (shared with the prompt + parser) ────────────────
def classified(predicate: Callable[[float], bool]) -> str:
    """Return ``"yes"/"no"`` for a boolean predicate.

    Used to keep the LLM output vocabulary small and parseable (classification
    predicates evaluate to literal "yes"/"no", never free prose).
    """
    return "yes" if predicate else "no"
