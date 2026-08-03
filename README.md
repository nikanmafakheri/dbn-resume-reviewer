# DBN Resume Reviewer

AI-powered resume reviewer — **completely free**, single-page web app. Upload your resume (PDF/DOCX), get an AI evaluation with multiple scores (ATS, skills, experience, formatting, content + overall **DBN score**), a Persian analysis paragraph, and actionable improvement feedback. Scroll down for a downloadable **DBN Standard resume template** (.pptx).

## Tech Stack

- **Backend**: Python 3.12, FastAPI, SQLAlchemy 2.0 async, SQLite (dev) / PostgreSQL (Docker)
- **Frontend**: React 19, TypeScript, Vite, Tailwind CSS — single-page, bilingual (EN/FA), RTL
- **AI**: Multi-provider (Gemini default, OpenAI, Claude, OpenRouter), free Gemini tier key
- **Queue**: Celery + Redis (configured; MVP scores inline)
- **Auth**: none — the app is anonymous (no accounts, no JWT)

## Quick Start

```bash
# Backend
cd backend
cp .env.example .env    # set GEMINI_API_KEY
uv run uvicorn app.main:app --reload   # uses SQLite by default

# Frontend
cd frontend
npm install
npm run dev
```

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- Frontend: http://localhost:3000

## Tests & Lint

```bash
cd backend
uv run pytest          # 39 unit/integration tests
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
