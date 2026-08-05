# Friendly "Quota Exhausted / Please Wait" UX

## Context

The app scores resumes via the Gemini **free tier**. When the free-tier quota hits 100% (as it has now), live analyses return a `failed` analysis whose `error_message` is the raw Gemini SDK string:

> `Gemini request failed: 429 You exceeded your current quota...`

Today that raw text is dumped to the user verbatim at `frontend/src/components/features/AnalysisResults.tsx:185`, inside a generic red "Analysis Failed" card. There is no way to tell a quota pause from a real bug, no friendly "please wait," and no affordance to retry without re-uploading. A second, unrelated 429 (the API's own rate-limiter middleware) is currently masked entirely by `App.tsx`'s generic `'Upload failed'` / `'Analysis trigger failed'` errors.

**Goal:** when quota is exhausted (or the API rate-limit trips), show a friendly, localized amber "we're at capacity — please wait" card with a retry countdown + manual Try Again, and preserve the user's uploaded resume so they don't have to re-upload. A real bug still shows the existing red failure card.

Decisions (confirmed with user): **backend `error_code` field** for structured detection; **explain + wait + retry** card; **cover both 429s** (Gemini quota + middleware rate-limit).

## Backend changes

### 1. Structured error classification
- **`backend/app/core/exceptions.py`** (or new `backend/app/ai/exceptions.py`): add a `ProviderRateLimitError(RuntimeError)` marker class (carries `provider` + `status_code`).
- **`backend/app/ai/providers/base.py`**: add a small helper (e.g. `def is_rate_limit_error(exc) -> bool`) or have providers raise the marker. Simplest: in each provider's `except` block, when the wrapped message contains `429`/`quota`/`rate limit`/`exceeded` (reuse one shared regex), raise `ProviderRateLimitError` instead of bare `RuntimeError`. Files: `gemini.py`, `openai.py`, `claude.py`, `openrouter.py` — same pattern, list one as representative.

### 2. `error_code` column + API field
- **Model** `backend/app/domain/models/analysis.py`: add `error_code: Mapped[str | None] = mapped_column(String(50), nullable=True)` next to `error_message`.
- **Migration** `backend/migrations/versions/0004_analysis_error_code.py` (revision `0004`, `down_revision = "0003"`): `op.add_column("analyses", sa.Column("error_code", sa.String(50), nullable=True))` — pure additive, no data migration (same shape as 0003).
- **Schema** `backend/app/schemas/analysis.py` `AnalysisResponse`: add `error_code: str | None = None`.
- **Set it** where errors are recorded — both places:
  - `backend/app/api/v1/resumes.py` `analyze_resume` (inline path, ~line 99)
  - `backend/app/services/analysis_service.py` `run_analysis` (Celery path, line 37-39)
  - Pattern: `analysis.error_code = "rate_limited" if isinstance(exc, ProviderRateLimitError) else None` (leave None for real bugs).

### 3. Middleware 429 exposure (the *other* 429)
The rate-limit middleware returns `HTTPException(429, "Too many requests")` — FastAPI's default handler already produces `{"detail": "Too many requests"}` with status 429. No backend change needed; the frontend just needs to check `res.status === 429`. (Confirm the default exception handler passes through — it does, since `AppException` handler only intercepts `AppException`.)

## Frontend changes

### 4. i18n keys
Add a `quota` group to **`frontend/src/i18n/en.json`** and **`frontend/src/i18n/fa.json`** (Persian translations), e.g.:
```json
"quota": {
  "title": "We're at capacity right now",
  "body": "The free AI tier is maxed out — many people are analyzing right now. Please wait a minute and try again.",
  "waiting": "Retrying in {seconds}s",
  "retryNow": "Try Again Now",
  "keepResume": "Your resume is saved — no need to re-upload."
}
```
Then regenerate the typed union: `cd frontend && node scripts/gen-i18n-types.mjs` (updates `src/types/i18n.ts`).

### 5. Rate-limit helper + upload 429 handling
- `frontend/src/lib/api.ts`: add an exported `isRateLimitError(statusOrMessage)` helper (checks `status === 429` or message matches `/quota|rate limit|exceeded/i`).
- `frontend/src/App.tsx` `handleFile` (lines 25-46): currently throws generic `'Upload failed'` / `'Analysis trigger failed'`, dropping the 429 detail. Change to read `res.status` — when `429`, surface the quota message via `setUploadError(...)` (localized key) instead of the generic string. Optionally short-circuit before calling analyze.

### 6. Quota-friendly failure card in `AnalysisResults.tsx`
- Add a `useLanguage`-driven **quota state** branch between the `failed` and `error` branches (before line 176):
  - If `data.status === 'failed' && data.error_code === 'rate_limited'` (or `isRateLimitError(data.error_message)`) → render the **amber wait card** (reuse `card-flat` + `badge-warning` + existing spinner pattern; no red `--danger`).
  - Include: friendly title + body, a live **countdown** ("Retrying in {n}s", e.g. 30 → 0), the resume is preserved (no re-upload needed — the analysis row still exists), a manual **Try Again Now** button.
  - Auto-retry: after countdown, call `onRetry` (re-fetch same `analysisId`) rather than resetting to upload — note `handleRetry` currently only does `setAnalysisId(null)`; it must be changed to **re-trigger polling** on the existing analysis (see step 7).
  - Keep the red `failed` card for `error_code` that is null/unknown (real bugs).

### 7. Retry semantics in `App.tsx`
- Change `handleRetry` (lines 51-53) from `setAnalysisId(null)` to re-query the *existing* `analysisId` — simplest correct approach: re-render `AnalysisResults` with the same id via a retry nonce, or have `AnalysisResults` re-run its polling effect when `onRetry` bumps an internal `retryKey`. Since the backend creates a fresh `Analysis` row each `POST /resumes/{id}/analyze`, a true "retry same analysis" is not available; the pragmatic, user-friendly option is: on retry, call `POST /resumes/{id}/analyze` again to create a new analysis and set `analysisId` to the new id (keeps the uploaded resume, re-runs scoring). This also aligns with "wait + try again."

## Files touched (representative)
- Backend: `app/ai/providers/{base,gemini,openai,claude,openrouter}.py`, `app/domain/models/analysis.py`, `app/api/v1/resumes.py`, `app/services/analysis_service.py`, `app/schemas/analysis.py`, `migrations/versions/0004_*.py`
- Frontend: `src/i18n/en.json`, `src/i18n/fa.json`, `src/types/i18n.ts` (generated), `src/lib/api.ts`, `src/App.tsx`, `src/components/features/AnalysisResults.tsx`

## Verification
1. **Backend unit**: `cd backend && uv run pytest -q` — still 42 passing. Add a small unit test asserting a quota-scenario error sets `error_code = "rate_limited"` (stub a provider raising `ProviderRateLimitError`; extend `tests/integration/test_analysis_flow.py` pattern already asserting `error_message`).
2. **Migration**: `uv run alembic upgrade head` (SQLite dev) and offline `--sql` against Postgres shows `ALTER TABLE analyses ADD COLUMN error_code`.
3. **Frontend build**: `cd frontend && npm run build` — `tsc -b && vite build` exit 0 (i18n type union regenerated; new keys type-check).
4. **Quota card manually**: temporarily set `LLM_PROVIDER` path to raise `ProviderRateLimitError` (or run against the live 429 quota), upload → analyze → observe amber "wait & retry" card with countdown; confirm no re-upload needed and Try Again creates a new analysis. Verify the middleware 429 by hammering `/resumes/upload` > 60 req/min → friendly quota message instead of generic failure.
5. **Regression**: red failure card still appears for a genuine error (e.g. no API key → `RuntimeError`) — `error_code` stays null.
