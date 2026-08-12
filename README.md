<div align="center">

<br />

<img src="images/logo.jpg" alt="DBN Resume Reviewer" width="140" height="140" style="border-radius: 24px;" />

<br />

# 📄 DBN Resume Reviewer

**AI-powered, 5-dimensional resume evaluation for software engineering candidates & technical recruiters.**

[![Website](https://img.shields.io/badge/Website-dbnresumereviewer.vercel.app-0A84FF?style=flat-square&logo=vercel&logoColor=white)](https://dbnresumereviewer.vercel.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

<br />

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-6.0-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-8-BD34FE?style=for-the-badge&logo=vite&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4.3-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![Neon Postgres](https://img.shields.io/badge/Neon_Postgres-Serverless-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)

<br />

[🚀 Quick Start](#-quick-start-local-development) • [🧮 Scoring System](#-scoring-system--evaluation-philosophy) • [🔌 API Reference](#-api-endpoints-reference) • [☁️ Deployment](#-production-deployment)

</div>

---

## 🎯 Overview

**DBN Resume Reviewer** is a free, single-page web application designed to evaluate, score, and optimize resumes specifically for software engineering and technical roles. 

Unlike generic resume tools that generate random or hallucinated scores, **DBN Resume Reviewer** uses a **deterministic 5-dimensional scoring model** powered by serverless LLM inference (Qwen3.6-35B-A3B-FP8 via the InferX gateway). It guarantees that overall scores are calculated mathematically server-side using strict weighted formulas.

Additionally, it provides bilingual analysis (English summary + native Persian recruiter feedback) tailored to the Iranian tech hiring landscape, and offers a downloadable **DBN Standard Resume Template (.pptx)** based on minimal ATS-friendly guidelines.

---

## 🌟 Key Features

| Feature | Description |
|---|---|
| **🎯 5-Dimensional AI Scoring** | Evaluates resumes across ATS Compatibility (25%), Skills Depth (25%), Experience Impact (25%), Formatting Quality (10%), and Writing Content (15%). |
| **🧮 Deterministic Overall Score** | The overall score is calculated server-side using strict weighted mathematical formulas—eliminating AI hallucination. |
| **📝 Recruiter-Grade Insights** | Generates grounded strengths, specific weaknesses, missing technical skills, and prioritized actionable recommendations. |
| **🌐 Bilingual & Persian Tech Context** | Delivers concise English summaries alongside professional Persian (فارسی) recruiter analysis tailored for Iranian tech hiring. |
| **📏 Standing Recruiter Rules** | Enforces 1–2 page limits, English language compliance, absence of visual charts/diagrams, minimal design, and software engineering alignment. |
| **📄 DBN Standard Template (.pptx)** | One-click download of an ATS-optimized, minimalist PowerPoint resume template designed according to DBN standards. |
| **⚡ Zero-Friction Anonymous MVP** | Immediate upload and analysis without requiring sign-up, registration, or JWT authentication barriers. |
| **🌓 Dark / Light Mode & Native RTL** | Smooth theme toggling, custom design tokens, score gauge rings, and automatic Persian RTL layout switching. |

---

## 📐 Architecture & Technology Stack

```
                          ┌─────────────────────────┐
                          │   React 19 + Vite UI    │
                          │  (TypeScript + Tailwind)│
                          └────────────┬────────────┘
                                       │ HTTP / REST
                                       ▼
                          ┌─────────────────────────┐
                          │     FastAPI Backend     │
                          │      (Python 3.12)      │
                          └─────┬──────────────┬────┘
                                │              │
            SQLAlchemy 2.0      │              │ Async HTTP / JSON
              (asyncpg)         ▼              ▼
        ┌─────────────────────────┐  ┌───────────────────────────┐
        │ Neon Serverless Postgres│  │  InferX GPU API Gateway   │
        │   (TLS / sslmode=require)│  │ (Qwen3.6-35B-A3B-FP8)     │
        └─────────────────────────┘  └───────────────────────────┘
```

### Stack Breakdown

- **Backend**: Python 3.12, FastAPI 0.115+, SQLAlchemy 2.0 (async), Pydantic v2, Alembic
- **Database**: Serverless PostgreSQL on Neon (`postgresql+asyncpg://` with TLS `sslmode=require`)
- **LLM Provider**: InferX OpenAI-compatible API Gateway (`https://model.inferx.net/endpoints/v1`), running the `Qwen3.6-35B-A3B-FP8` model
- **Frontend**: React 19, TypeScript 6.0, Vite 8, Tailwind CSS 4.3, Oxlint
- **Task Orchestration**: Celery & Redis (development/docker environment), synchronous execution on serverless deployments (Vercel/Render)
- **Deployment**: Monorepo configuration on Vercel (`vercel.json`) & Blueprint deployment on Render (`render.yaml`)

---

## 📊 Scoring System & Evaluation Philosophy

The evaluation pipeline follows a strict, deterministic scoring rubric defined in `backend/app/core/scoring.py`.

### 1. Mathematical Score Formula

$$\text{Overall Score} = (0.25 \times \text{ATS}) + (0.25 \times \text{Skills}) + (0.25 \times \text{Experience}) + (0.10 \times \text{Formatting}) + (0.15 \times \text{Content})$$

| Dimension | Weight | Primary Criteria Evaluated |
|---|---|---|
| **ATS Compatibility** | `25%` | Machine-readable headings, keyword coverage, language (English), length (1-2 pages) |
| **Skills Depth** | `25%` | Structured taxonomy, relevance to software engineering, tool & framework proficiency |
| **Experience Impact** | `25%` | Action-oriented verbs, quantified achievements/metrics, career progression |
| **Formatting** | `10%` | Visual hierarchy, 1-2 page maximum, minimal design, zero visual charts/graphs |
| **Content Quality** | `15%` | Concise writing, error-free grammar, presence of education, links, and certifications |

> [!NOTE]
> **Absent Section Policy**: Missing sections on a resume are scored within a realistic 40–70 range (never hard-floored at 0). This ensures a missing section penalizes the score without completely destroying an otherwise strong candidate's overall result.

---

## 🚀 Quick Start (Local Development)

### Prerequisites

- **Python 3.12+** with [`uv`](https://github.com/astral-sh/uv) installed
- **Node.js 18+** & `npm`
- A **Neon PostgreSQL** database connection string
- An **InferX API Key**

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Copy environment variables example
cp .env.example .env

# Configure .env with your credentials:
# DATABASE_URL=postgresql+asyncpg://USER:PASSWORD@HOST.neon.tech/neondb?sslmode=require
# INFERX_API_KEY=your_inferx_api_key

# Run Alembic migrations
uv run alembic upgrade head

# Start FastAPI server
uv run uvicorn app.main:app --reload --port 8000
```

- **API Base**: `http://localhost:8000/api/v1`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/health`

### 2. Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install packages
npm install

# Start Vite dev server
npm run dev
```

- **Web App**: `http://localhost:3000`

---

## 🐳 Docker Setup

For a complete local environment including Redis and Celery background workers:

```bash
# Start all services
docker-compose up --build
```

Services initialized:
- **FastAPI API**: `http://localhost:8000`
- **Redis**: `localhost:6379`
- **Celery Worker & Celery Beat**

---

## 🔌 API Endpoints Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/resumes/upload` | Upload a PDF resume (max 10 MB) and extract raw text |
| `GET` | `/api/v1/resumes` | List all uploaded resumes |
| `DELETE` | `/api/v1/resumes/{id}` | Delete a resume and its associated analysis |
| `POST` | `/api/v1/resumes/{id}/analyze` | Trigger 5-dimensional evaluation |
| `GET` | `/api/v1/analysis/{id}` | Retrieve evaluation status and detailed score results |
| `GET` | `/api/v1/dbn-standards/template/download` | Download the DBN Standard PowerPoint template (`.pptx`) |
| `GET` | `/health` | Server health check endpoint |

---

## 🔧 Environment Variables Reference

### Backend (`backend/.env`)

```ini
APP_NAME="DBN Resume Reviewer"
DEBUG=false
DATABASE_URL="postgresql+asyncpg://USER:PASSWORD@HOST.neon.tech/neondb?sslmode=require"
INFERX_API_KEY="your_inferx_api_key"
INFERX_BASE_URL="https://model.inferx.net/endpoints/v1"
INFERX_MODEL="Qwen3.6-35B-A3B-FP8"
CORS_ORIGINS='["http://localhost:3000"]'
REDIS_URL="redis://localhost:6379/0"
```

### Frontend (`frontend/.env`)

```ini
VITE_API_BASE_URL="/api/v1"
```

---

## ☁️ Production Deployment

### Vercel (Monorepo)
The root `vercel.json` configures unified hosting:
- Frontend static build from `frontend/`
- Backend Python serverless function from `backend/app/main:app`
- `/api/*` rewrites routed to the Python service.

### Render (Blueprint)
The root `render.yaml` provisions Render's free tier:
- `dbn-resume-api`: Docker Web Service
- `dbn-resume-web`: Static React Site

---

## 🧪 Testing & Code Quality

```bash
# Backend Linting
cd backend
uv run ruff check .

# Backend Testing (Requires TEST_DATABASE_URL)
TEST_DATABASE_URL="postgresql+asyncpg://user:pass@host/dbn_resume_test?sslmode=require" uv run pytest

# Frontend Build & Typecheck
cd frontend
npm run build

# Frontend Linting
npm run lint
```

---

## 📜 License

This project is open-source and released under the [MIT License](LICENSE). Built for software engineering candidates, technical recruiters, and hiring teams.
