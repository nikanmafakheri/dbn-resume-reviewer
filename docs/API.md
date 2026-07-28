# API Reference

Base URL: `/api/v1`

## Authentication

All endpoints except `/auth/register` and `/auth/login` require a Bearer JWT token in the `Authorization` header.

### POST /auth/register
Register a new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecureP@ss1",
  "full_name": "John Doe"
}
```

**Response (201):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "candidate",
  "is_active": true
}
```

### POST /auth/login
Authenticate and receive JWT tokens.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecureP@ss1"
}
```

**Response (200):**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

### POST /auth/refresh
Exchange a valid refresh token for a new token pair.

## Users

### GET /users/me
Get the authenticated user's profile.

### PATCH /users/me
Update profile fields (e.g., `full_name`).

## Resumes

### POST /resumes/upload
Upload a resume file. Accepts `multipart/form-data` with a `file` field.
- Allowed types: `.pdf`, `.doc`, `.docx`
- Max size: 10 MB

### GET /resumes
List all resumes for the authenticated user.

### DELETE /resumes/{id}
Delete a resume. Must own the resume.

### POST /resumes/{id}/analyze
Trigger AI analysis. Returns 202 Accepted with the analysis record. Processing happens asynchronously via Celery.

## Analysis

### GET /analysis/{id}
Get analysis results. Poll this endpoint while status is `pending` or `processing`.

## DBN Standards

### GET /dbn-standards
Get the currently active scoring standard.

### POST /dbn-standards
Create a new scoring standard.