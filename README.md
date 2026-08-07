# DBN Resume Reviewer

AI-powered resume reviewer — **completely free**, single-page web app. Upload your resume (PDF), get an AI evaluation with multiple scores (ATS, skills, experience, formatting, content + overall **DBN score**), a Persian analysis paragraph, and actionable improvement feedback. Scroll down for a downloadable **DBN Standard resume template** (.pptx).

## Tech Stack

- **Backend**: Python 3.12, FastAPI, SQLAlchemy 2.0 async, PostgreSQL (Neon)
- **Frontend**: React 19, TypeScript, Vite, Tailwind CSS — single-page, bilingual (EN/FA), RTL
- **AI**: InferX (OpenAI-compatible gateway, Qwen3.6-35B-A3B-FP8) — single provider
- **Queue**: none on deploy — scoring runs inline; Redis/Celery are optional dev-only extras
- **Auth**: none — the app is anonymous (no accounts, no JWT)

## Quick Start

```bash
# Backend (requires a Neon PostgreSQL DATABASE_URL in backend/.env)
cd backend
cp .env.example .env
uv run alembic upgrade head
uv run uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- Frontend: http://localhost:3000

## Deploy (Render free tier)

Two free services (see `render.yaml`), each deploys automatically on push to `main`:

- **API** — Docker web service. Migrations run at startup (`alembic upgrade head`
  when `DEBUG != "true"`); set `DATABASE_URL` and `INFERX_API_KEY` in the dashboard.
- **Web** — static React site pointing at the API via `VITE_API_BASE_URL`.

No Redis is provisioned — the rate limiter falls back to in-memory and scoring is
synchronous.

## Tests & Lint

```bash
cd backend
uv run pytest          # unit/integration/e2e tests
uv run ruff check .    # lint

cd frontend
npm run build          # tsc + vite production build
npm run lint           # oxlint
```

## Project Structure

```
backend/
  app/
    api/v1/        # Route handlers (resumes, analysis, dbn-standards)
    ai/            # LLM providers, scorer, parser, prompts
    core/          # Config, scoring, database, security
    domain/models/ # SQLAlchemy ORM models
    repositories/  # Data access layer
    services/      # Business logic
    middleware/    # CORS, rate limiting, logging
    workers/       # Celery background tasks
  tests/
frontend/
  src/
    components/    # UI primitives, features, layout
    context/       # Theme + language (EN/FA)
    i18n/          # en.json, fa.json
    lib/           # typed API client
    types/         # TypeScript interfaces
```

## Scoring

Evaluates five dimensions — ATS (25%), Skills (25%), Experience (25%), Formatting (10%), Content (15%). The **overall score is computed deterministically** server-side as a weighted mean; the LLM supplies only per-dimension scores and justifications. See `docs/SCORING.md`.

## License / Support

Open source. If this tool saves you time, consider supporting the author: https://github.com/sponsors/safishamsi
