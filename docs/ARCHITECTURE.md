# Architecture

## Layered Design

```
┌─────────────────────────────────────┐
│         FastAPI (main.py)           │
│  Middleware: CORS, Logging, Rate    │
├─────────────────────────────────────┤
│         API v1 Routes               │
│  auth  users  resumes  analysis     │
│         dbn-standards               │
├─────────────────────────────────────┤
│         Services Layer              │
│  AuthService  ResumeService         │
│  AnalysisService  ScoringService    │
│  DBNStandardService  EmailService   │
├─────────────────────────────────────┤
│         Repository Layer            │
│  CRUD per entity (BaseRepository)   │
├─────────────────────────────────────┤
│    Domain Models (SQLAlchemy ORM)   │
│  User  Resume  Analysis  DBNStandard│
├─────────────────────────────────────┤
│         AI Layer                    │
│  Providers (Gemini/OpenAI/Claude)    │
│  Scorers → Parsers → Prompts        │
├─────────────────────────────────────┤
│         Celery Workers              │
│  Analysis  Emails  Cleanup          │
└─────────────────────────────────────┘
```

## Data Flow

1. User uploads a resume (PDF) → stored in `media/resumes/`
2. PDF text extracted via PyMuPDF → stored as `text_content`
3. Analysis triggered → Celery task dispatched with 202 response
4. Celery worker loads resume text, calls configured AI provider
5. AI returns structured JSON → parsed, validated, persisted
6. Frontend polls `GET /analysis/{id}` → displays score gauges on completion

## Key Design Decisions

- **Async everything**: FastAPI async endpoints + async SQLAlchemy 2.0 + async LLM calls
- **Repository pattern**: Clean data access abstraction for testability
- **Factory pattern for AI**: Swap LLM backend via `LLM_PROVIDER` env var (Gemini/OpenAI/Claude/OpenRouter)
- **JWT with refresh tokens**: 30-minute access tokens + 7-day refresh tokens with transparent frontend refresh
- **Celery for async workloads**: Analysis runs in background, API responds immediately
- **Rate limiting**: Redis sliding-window with in-memory fallback for resilience