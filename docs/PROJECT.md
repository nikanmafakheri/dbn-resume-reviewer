# Project Overview

## DBN Resume Reviewer

An AI-powered resume reviewer that scores resumes across five dimensions and returns actionable feedback plus a downloadable DBN Standard template. It is a **completely free, anonymous, single-page app** that uses the free Gemini tier.

## Repository Structure

```
resume-reviewer/
  backend/          # FastAPI + SQLAlchemy async + AI providers
  frontend/         # React 19 + Vite + TypeScript (single-page SPA)
  docs/             # Documentation
  images/           # UI mockups and design concepts
  dbn-standard-resume-template/  # downloadable .pptx template
  docker-compose.yml
  README.md
```

## Key Features

- Resume upload (PDF, DOCX) with size/type validation
- AI scoring across five dimensions: ATS, Skills, Experience, Formatting, Content
  - Deterministic overall score (weighted mean, computed server-side)
  - Per-dimension justifications + strengths / weaknesses / missing skills / recommendations
  - Persian analysis paragraph + English summary
- Configurable AI providers (Gemini default, OpenAI, Claude, OpenRouter)
- DBN Standard scoring rubric + downloadable `.pptx` template
- Responsive, bilingual (EN/FA with RTL) single-page UI with animated score gauges
- Rate limiting (Redis or in-memory fallback)

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12, FastAPI, SQLAlchemy 2.0 async |
| Database | SQLite via `aiosqlite` (dev default) / PostgreSQL 16 via `asyncpg` (Docker) |
| Queue | Celery + Redis (configured; the MVP scores inline) |
| Frontend | React 19, TypeScript, Vite, Tailwind CSS |
| AI | Gemini, OpenAI, Claude, OpenRouter |
| Auth | none — anonymous |
| PDF | PyMuPDF |
| Container | Docker Compose (API + workers + Postgres + Redis) |

## Current Status

**Maturity:** solid, working anonymous MVP. The backend is fully tested (39 passing) and scoring is deterministic and explainable. The frontend production build and lint are green.

**Scope note:** this is the anonymous single-page MVP. It is **not** (and is not documented as) the JWT-authenticated multi-page SaaS — auth was deliberately removed. See `docs/SCORING.md` and `docs/ROADMAP.md`.