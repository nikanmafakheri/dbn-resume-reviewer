# Database Schema

## Tables

### users
| Column | Type | Notes |
|--------|------|-------|
| id | UUID | PK |
| email | VARCHAR(255) | Unique, indexed |
| password_hash | VARCHAR(255) | bcrypt hash |
| full_name | VARCHAR(255) | Nullable |
| role | VARCHAR(50) | candidate, recruiter, admin |
| is_active | BOOLEAN | Default true |
| created_at | TIMESTAMPTZ | Auto |
| updated_at | TIMESTAMPTZ | Auto |

### resumes
| Column | Type | Notes |
|--------|------|-------|
| id | UUID | PK |
| user_id | UUID | FK → users.id |
| filename | VARCHAR(255) | Stored filename |
| original_filename | VARCHAR(255) | Upload name |
| file_path | VARCHAR(512) | Filesystem path |
| file_size_bytes | BIGINT | Nullable |
| mime_type | VARCHAR(100) | Nullable |
| status | VARCHAR(50) | pending/processing/completed/failed |
| text_content | TEXT | Extracted PDF text |
| metadata | JSON | Nullable |

### analyses
| Column | Type | Notes |
|--------|------|-------|
| id | UUID | PK |
| resume_id | UUID | FK → resumes.id |
| user_id | UUID | FK → users.id |
| dbn_standard_id | UUID | FK → dbn_standards.id (nullable) |
| status | VARCHAR(50) | pending/processing/completed/failed |
| overall_score | FLOAT | Nullable |
| ats_score | FLOAT | Nullable |
| grammar_score | FLOAT | Nullable |
| recruiter_score | FLOAT | Nullable |
| summary | TEXT | Nullable |
| feedback_json | JSON | Nullable |
| error_message | TEXT | Nullable |
| processing_time_ms | INTEGER | Nullable |

### dbn_standards
| Column | Type | Notes |
|--------|------|-------|
| id | UUID | PK |
| name | VARCHAR(255) | |
| description | TEXT | Nullable |
| version | VARCHAR(20) | |
| is_active | BOOLEAN | Default true |
| created_by | UUID | FK → users.id |

### dbn_standard_criteria
| Column | Type | Notes |
|--------|------|-------|
| id | UUID | PK |
| dbn_standard_id | UUID | FK → dbn_standards.id |
| name | VARCHAR(255) | |
| description | TEXT | Nullable |
| weight | FLOAT | |
| max_score | FLOAT | |
| sort_order | INTEGER | |

## ER Diagram

```
users 1──N resumes
users 1──N analyses
resumes 1──N analyses
dbn_standards 1──N dbn_standard_criteria
dbn_standards N──1 analyses (optional)
```