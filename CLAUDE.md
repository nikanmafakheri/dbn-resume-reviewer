# DBN Resume Reviewer

## Project Overview
AI-powered SaaS platform for analyzing and scoring resumes. FastAPI backend + React frontend.

## Commands
- Backend: `cd backend && uv run uvicorn app.main:app --reload`
- Frontend: `cd frontend && npm run dev`
- Tests: `cd backend && uv run pytest`
- Migrations: `cd backend && alembic upgrade head`
- Build frontend: `cd frontend && npm run build`

## Architecture
- Backend: Python 3.12, FastAPI, SQLAlchemy 2.0 async, PostgreSQL, Celery, Redis
- Frontend: React 19, TypeScript, Vite, Tailwind CSS, Axios, React Router 6
- Multi-AI-provider: Gemini (default), OpenAI, Claude, OpenRouter

## Key Files
- `backend/app/main.py` — FastAPI app factory
- `backend/app/core/config.py` — Settings (env vars)
- `backend/app/dependencies.py` — DI wiring
- `backend/app/api/v1/` — All route handlers
- `backend/app/ai/` — LLM providers, prompts, parsers
- `frontend/src/App.tsx` — Frontend routing
- `docker-compose.yml` — Full stack orchestration

## Status
Phase 1-3 (backend) and Phase 4 (frontend) complete. See docs/ROADMAP.md.