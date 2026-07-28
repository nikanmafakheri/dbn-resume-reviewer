# Project Overview

## DBN Resume Reviewer

An AI-powered SaaS platform that analyzes resumes and provides actionable scoring feedback across four dimensions.

## Repository Structure

```
resume-reviewer/
  backend/          # FastAPI + SQLAlchemy + Celery
  frontend/         # React 19 + Vite + TypeScript
  docs/             # Documentation
  images/           # UI mockups and design concepts
  docker-compose.yml
  README.md
```

## Key Features

- Resume upload (PDF, DOC, DOCX)
- AI-powered scoring (ATS, Grammar, Recruiter, Overall)
- Configurable AI providers (Gemini, OpenAI, Claude, OpenRouter)
- Background processing via Celery
- JWT authentication with refresh tokens
- DBN Standard scoring rubrics
- Responsive web UI with animated score gauges

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12, FastAPI, SQLAlchemy 2.0 |
| Database | PostgreSQL 16 (async via asyncpg) |
| Queue | Celery + Redis |
| Frontend | React 19, TypeScript, Vite, Tailwind CSS |
| AI | Gemini, OpenAI, Claude, OpenRouter |
| Auth | JWT (python-jose + bcrypt) |
| PDF | PyMuPDF |
| Container | Docker Compose (API + workers + Postgres + Redis) |