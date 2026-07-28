# Scoring System

## Four Score Dimensions

Each score ranges from **0 to 100**.

| Dimension | What It Measures |
|-----------|-----------------|
| **Overall** | Composite evaluation of the entire resume |
| **ATS** | Compatibility with Applicant Tracking Systems (keywords, formatting, sections) |
| **Grammar** | Spelling, grammar, punctuation, writing style |
| **Recruiter** | Subjective appeal to human recruiters (impact, clarity, achievements) |

## Color Coding

| Score Range | Color | Meaning |
|-------------|-------|---------|
| 0–49 | Red | Needs significant improvement |
| 50–74 | Yellow | Average, room for improvement |
| 75–100 | Green | Strong / Excellent |

## How It Works

1. Resume text is sent to an AI LLM with the `resume_analysis.md` prompt
2. The LLM returns a JSON object with all four scores, a summary, and optional feedback
3. Scores are validated by `ScoreParser` into a `ScoreResult` Pydantic model
4. Results are stored in the `analyses` table for retrieval via the API

## Prompt Templates

- `resume_analysis.md` — Main scoring prompt (4 dimensions)
- `ats.md` — Detailed ATS compatibility analysis with issues/recommendations
- `grammar.md` — Grammar/style analysis with typed issue list
- `cover_letter.md` — Cover letter generation from resume + job description