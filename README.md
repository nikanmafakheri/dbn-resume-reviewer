# DBN Resume Reviewer

AI-powered SaaS platform for analyzing and scoring resumes. Upload your resume, get instant AI feedback across four dimensions: ATS compatibility, grammar/style, recruiter appeal, and overall score.

## Tech Stack

- **Backend**: Python 3.12, FastAPI, SQLAlchemy 2.0 async, PostgreSQL, Celery, Redis
- **Frontend**: React 19, TypeScript, Vite, Tailwind CSS, React Router 6
- **AI**: Multi-provider (Gemini, OpenAI, Claude, OpenRouter)
- **Auth**: JWT (access + refresh tokens), bcrypt

## Quick Start

```bash
# Backend
cd backend
cp .env.example .env    # edit your API keys
docker compose up -d     # starts PostgreSQL + Redis
alembic upgrade head
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- Frontend: http://localhost:3000

## Project Structure

```
backend/
  app/
    api/v1/        # Route handlers
    ai/            # LLM providers, scorers, parsers, prompts
    core/          # Config, security, database, logging
    domain/models/ # SQLAlchemy ORM models
    repositories/  # Data access layer
    services/      # Business logic
    middleware/    # CORS, rate limiting, logging
    workers/       # Celery background tasks
  tests/
frontend/
  src/
    api/           # Axios client + endpoint modules
    components/    # UI primitives, features, layout
    context/       # Auth state management
    hooks/         # Custom React hooks
    pages/         # Route-level components
    types/         # TypeScript interfaces
```