# API Reference

Base URL: `/api/v1`

The app is **anonymous** — no authentication is required (or present) on any endpoint. Every record is tagged with a shared `ANONYMOUS_USER_ID`.

## Resumes

### POST /resumes/upload
Upload a resume file. Accepts `multipart/form-data` with a `file` field.

- Allowed types: `.pdf` (rejected otherwise → 400)
- Max size: **10 MB** → 400 beyond
- PDF text is extracted at upload (failure to extract is logged, not fatal)
- Returns the created `ResumeResponse`

**Response (201):**
```json
{
  "id": "uuid",
  "filename": "uuid.pdf",
  "original_filename": "resume.pdf",
  "file_size_bytes": 2048,
  "mime_type": "application/pdf",
  "status": "uploaded",
  "text_content": "..."
}
```

### GET /resumes
List all uploaded resumes.

### DELETE /resumes/{id}
Delete a resume by ID. Returns 204. 404 if not found.

### POST /resumes/{id}/analyze
Trigger an AI analysis. **Runs inline** (no background worker in the MVP); failures are recorded on the analysis row, never swallowed.

**Response (202):** an `AnalysisResponse` snapshot.

States: `pending` → `completed` | `failed`.

## Analysis

### GET /analysis/{id}
Get analysis results. The frontend polls this endpoint every ~3 s while status is `pending`, until `completed` or `failed`. 404 if not found; 422 on a malformed (non-UUID) id.

**Response (200):**
```json
{
  "id": "uuid",
  "resume_id": "uuid",
  "status": "completed",
  "ats_score": 82,
  "skills_score": 74,
  "experience_score": 68,
  "formatting_score": 90,
  "content_score": 71,
  "overall_score": 77,
  "summary": "…",
  "analysis_fa": "…persian paragraph…",
  "feedback": { "strengths": [], "weaknesses": [], "missing_skills": [], "recommendations": [] },
  "error_message": null,
  "processing_time_ms": 3456
}
```

## DBN Standards

### GET /dbn-standards/template/download
Download the DBN Standard resume template as a `.pptx` file (`FileResponse`). 404 if the template file is missing.

### GET /dbn-standards
Get the currently active scoring standard (rubric + criteria).

### POST /dbn-standards
Create a new scoring standard.

```json
{
  "name": "DBN Resume Standard v2",
  "version": "2.0",
  "description": "…"
}
```

## Notes

- **Scoring** runs inline in the `/resumes/{id}/analyze` route. The **overall score is deterministic** — computed server-side as a weighted mean of the five dimensions; the LLM never supplies it.
- **Errors** are returned as `{"detail": "…"}` via `AppException` handlers (typed NotFound/Unauthorized/Forbidden/Conflict). Unauth/Forbidden are defined but unused since there's no auth.