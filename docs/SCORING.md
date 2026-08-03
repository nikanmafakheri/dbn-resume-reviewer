# Scoring System

## Five Score Dimensions

Each score ranges from **0 to 100** and **must be justified** by evidence in
the resume — the AI never invents a score.

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| **ATS Compatibility** | 25% | Keyword coverage, standard ATS-parseable section headings, machine-readable text |
| **Skills** | 25% | Depth and relevance of hard/soft skills, proficiency signals |
| **Experience** | 25% | Role relevance, quantified outcomes, action-oriented language, clarity of history |
| **Formatting** | 10% | Readable layout, consistent hierarchy, appropriate length, parse-safe structure |
| **Content Quality** | 15% | Clarity, concision, grammar/spelling, tailored summary, completeness |

Weights sum to **1.0**; they are defined once in `app/core/scoring.py` and are
the single source of truth shared by the prompt, parser, and scorer.

## DBN Overall Score — weighted formula

The **overall score is never read from the LLM**. It is computed
deterministically as the weighted mean of the five dimension scores:

```
overall = round(
    0.25 * ats +
    0.25 * skills +
    0.25 * experience +
    0.10 * formatting +
    0.15 * content
, 2)
```

Because every dimension is justified and the overall is a pure function of
those dimensions, the result is **consistent, fair, and explainable**: the
overall score can always be decomposed into exactly why each point was earned.

## Color Coding

| Score Range | Color | Meaning |
|-------------|-------|---------|
| 0–49 | Red | Needs significant improvement |
| 50–74 | Yellow | Average, room for improvement |
| 75–100 | Green | Strong / Excellent |

## Confidence

Every result carries a `confidence` value — a **structural** measure of how
much of the requested schema survived validation (not an LLM self-estimate):

- **high** — all five dimension justifications are substantive (≥ 40 chars)
- **medium** — a conforming but thin justification is present somewhere
- **low** — most justifications are thin

## How It Works

1. Resume text is sent to an LLM with the `resume_analysis.md` prompt, which
   specifies a **strict JSON schema** and the professional hiring rubric.
2. The LLM returns the five dimension scores with per-dimension justification,
   plus strengths, weaknesses, missing skills, actionable recommendations, an
   English summary (`summary_en`), and a **native Persian professional
   analysis** (`analysis_fa`) written for Iranian recruiters (150–250 words,
   non-generic, explains why the score was assigned).
3. `ScoreParser` **strictly validates** the response: every dimension must be
   present and 0–100, every justification non-empty. Malformed, missing, or
   out-of-range responses are **rejected** — never silently clamped.
4. `ResumeScorer` **retries** rejected responses (up to 2 corrective
   re-prompts embedding the exact validation error) before surfacing a failure.
5. The overall score is recomputed deterministically from the dimensions.
6. Results are stored in the `analyses` table (mirrored dimension columns plus
   the full nested `scores_json`) for retrieval via the API.

## Prompt Templates

- `resume_analysis.md` — Main scoring prompt (5 dimensions, strict JSON schema)
- `ats.md` — Detailed ATS compatibility analysis with issues/recommendations
- `grammar.md` — Grammar/style analysis with typed issue list
- `cover_letter.md` — Cover letter generation from resume + job description
