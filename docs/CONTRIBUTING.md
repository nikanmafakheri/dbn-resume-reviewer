# Contributing

## Development Setup

```bash
# Clone and enter the project
cd resume-reviewer

# Backend
cd backend
cp .env.example .env  # Fill in your API keys
docker compose up -d   # Start PostgreSQL + Redis
uv sync               # Install Python deps
alembic upgrade head  # Run migrations
uvicorn app.main:app --reload

# Frontend (in another terminal)
cd frontend
npm install
npm run dev
```

## Code Style

- Python: Ruff linting (line length 100), type annotations required
- TypeScript: Strict mode, interfaces for all data shapes
- All new code must include tests

## Pull Request Process

1. Create a feature branch from `master`
2. Write tests for new functionality
3. Ensure all existing tests pass
4. Update documentation if API changes
5. Submit PR with descriptive title and changes list

## What to Work On

Check `docs/ROADMAP.md` for the current development priorities or ask in the project issues.