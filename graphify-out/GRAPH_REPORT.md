# Graph Report - /home/nikan/Documents/resume-reviewer  (2026-08-02)

## Corpus Check
- 131 files · ~138,102 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 763 nodes · 1082 edges · 83 communities (71 shown, 12 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 187 edges (avg confidence: 0.76)
- Token cost: 5,370 input · 6,800 output

## Community Hubs (Navigation)
- Core Domain Constants & Enums
- ATS Scoring System
- Score Parsing Engine
- Resume Upload & Schema API
- Frontend Dependencies
- Auth & Security Utilities
- Frontend Internationalization
- TypeScript App Config
- Database Engine & Session
- Cover Letter Generation
- Node TSConfig
- Analysis Results UI
- Standard Section Components
- Analysis Domain & Scoring Service
- Exception Handling
- Landing & Footer Components
- Alembic Migrations
- AI Provider Implementations
- Rate Limiting Middleware
- Base LLM Provider
- DBN Standard API
- Base Repository
- Docker Compose Services
- Upload & CTA Components
- DBN Standard Repository
- Language Context (i18n)
- Frontend Type Definitions
- AI Provider Modules
- Analysis API Endpoints
- Standard Create Schema
- Resumes API Endpoints
- App Entry & Lifespan
- Lint Rules (oxlint)
- App Root & Theme Context
- React Brand Assets
- Social Icon Set
- SVG Icon Sprite
- i18n Type Generation
- Gemini Resume Mockup
- Resume Screenshot Mockup
- Settings & Configuration
- Dependency Injection
- Request Logging Middleware
- Hero Marketing Banner
- Common Schemas
- PDF Text Extraction
- Favicon & Brand Mark
- Hero Brand Theme
- Gemini Marketing Asset
- Resume Scorer
- Celery Analysis Worker
- Logo Brand Elements
- Test Factories
- Logo Identity
- Vite Build Assets
- Root TSConfig
- AI Package Init
- Domain Models Init
- Middleware Init
- Utils Init
- Workers Init
- DBN Icon Mark
- Frontend Constants
- ChatGPT UI Mockup
- Unidentified Photo
- Package Metadata

## God Nodes (most connected - your core abstractions)
1. `compilerOptions` - 18 edges
2. `Database` - 17 edges
3. `compilerOptions` - 15 edges
4. `SQLAlchemy 2.0 async` - 14 edges
5. `User` - 13 edges
6. `AnalysisService` - 13 edges
7. `react` - 13 edges
8. `useLanguage()` - 13 edges
9. `ResumeService` - 12 edges
10. `DBN Resume Reviewer` - 12 edges

## Surprising Connections (you probably didn't know these)
- `Frontend README (Vite template)` --references--> `Frontend Stack (React 19)`  [INFERRED]
  frontend/README.md → CLAUDE.md
- `API Service (compose)` --semantically_similar_to--> `API Service (backend compose)`  [INFERRED] [semantically similar]
  docker-compose.yml → backend/docker-compose.yml
- `Celery Worker Service (compose)` --semantically_similar_to--> `Celery Worker Service (backend compose)`  [INFERRED] [semantically similar]
  docker-compose.yml → backend/docker-compose.yml
- `Celery Beat Service (compose)` --semantically_similar_to--> `Celery Beat Service (backend compose)`  [INFERRED] [semantically similar]
  docker-compose.yml → backend/docker-compose.yml
- `PostgreSQL Database Service (compose)` --semantically_similar_to--> `PostgreSQL Database Service (backend compose)`  [INFERRED] [semantically similar]
  docker-compose.yml → backend/docker-compose.yml

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Resume Scoring Dimensions** — ats_compatibility, grammar_style, recruiter_appeal, overall_score [EXTRACTED 1.00]
- **Full-Stack Architecture** — backend_stack, frontend_stack, postgres_db, redis_cache [EXTRACTED 0.95]
- **AI Provider Ecosystem** — gemini, openai, claude_ai, openrouter [EXTRACTED 1.00]
- **Celery Task Infrastructure** — api_service, celery_worker_service, celery_beat_service, redis_cache [EXTRACTED 1.00]
- **AI Scoring Prompt Suite** — backend_app_ai_prompts_ats_prompt, backend_app_ai_prompts_grammar_prompt, backend_app_ai_prompts_resume_analysis_prompt, backend_app_ai_prompts_cover_letter_prompt [INFERRED 0.85]
- **Favicon Brand Fragment** — frontend_public_favicon, frontend_public_favicon_bolt_mark, frontend_public_favicon_purple_palette, frontend_public_favicon_brand_purpose [INFERRED 0.85]
- **SOCIAL_LINK_ICON_SET** — frontend_public_icons_bluesky, frontend_public_icons_discord, frontend_public_icons_github, frontend_public_icons_x [INFERRED 1.00]
- **Resume Scoring Dimensions** — ats_compatibility, grammar_style, recruiter_appeal, overall_score [EXTRACTED 1.00]
- **ATS Prompt JSON Output Contract** — backend_app_ai_prompts_ats_score, backend_app_ai_prompts_ats_issues, backend_app_ai_prompts_ats_recommendations [EXTRACTED 1.00]
- **Full-Stack Compose Services (top-level)** — docker_compose_api, docker_compose_celery_worker, docker_compose_celery_beat, docker_compose_db, docker_compose_redis [EXTRACTED 1.00]
- **Backend Compose Services** — backend_docker_compose_api, backend_docker_compose_celery_worker, backend_docker_compose_celery_beat, backend_docker_compose_db, backend_docker_compose_redis [EXTRACTED 1.00]
- **AI Provider Set** — gemini, openai, claude_ai, openrouter [EXTRACTED 1.00]
- **Resume Scoring Criteria** — backend_app_ai_prompts_resume_analysis_overall_score, backend_app_ai_prompts_resume_analysis_ats_score, backend_app_ai_prompts_resume_analysis_grammar_score, backend_app_ai_prompts_resume_analysis_recruiter_score [INFERRED 0.95]
- **Frontend Technology Stack** — frontend_readme_react, frontend_readme_typescript, frontend_readme_vite [INFERRED 0.95]
- **Social / Brand Icon Set** — frontend_public_icons_bluesky_icon, frontend_public_icons_discord_icon, frontend_public_icons_github_icon, frontend_public_icons_social_icon, frontend_public_icons_x_icon, frontend_public_icons_documentation_icon [EXTRACTED 1.00]
- **DBN Resume Reviewer Brand Identity** — frontend_public_logo, frontend_public_logo_dbn, frontend_public_logo_scoring, frontend_public_logo_monochrome [INFERRED 0.85]
- **Hero Brand Visual Identity** — frontend_src_assets_hero, frontend_src_assets_hero_gem_ring, frontend_src_assets_hero_gradient_funnel, frontend_src_assets_hero_brand_violet [INFERRED 0.85]
- **React Logo Rendered as SVG** — frontend_src_assets_react_svg, frontend_src_assets_react_framework, iconify_logos, frontend_src_assets_react_brand_color [EXTRACTED 0.90]
- **Resume Composed of Standard Sections** — images_resume_header, images_resume_experience, images_resume_education, images_resume_skills [INFERRED 0.85]
- **Sample Resume Composed of Standard Sections** — images_gemini_generated_image_1tjqx1tjqx1tjqx1_header, images_gemini_generated_image_1tjqx1tjqx1tjqx1_experience, images_gemini_generated_image_1tjqx1tjqx1tjqx1_education, images_gemini_generated_image_1tjqx1tjqx1tjqx1_skills [INFERRED 0.85]

## Communities (83 total, 12 thin omitted)

### Community 0 - "Core Domain Constants & Enums"
Cohesion: 0.06
Nodes (31): Application-wide constants and enums., ResumeStatus, UserRole, Database, Manages the async SQLAlchemy engine and session factory., Create async SQLAlchemy engine with sensible defaults., Create tables (dev bootstrap) and seed defaults, idempotently.          In produ, get_resume_service() (+23 more)

### Community 1 - "ATS Scoring System"
Cohesion: 0.08
Nodes (40): API Service, Applicant Tracking System, ATS Compatibility, ats issues (list of strings), ATS Compatibility Prompt, ats recommendations (list of strings), ats_score (0-100), Cover Letter Generation (+32 more)

### Community 2 - "Score Parsing Engine"
Cohesion: 0.09
Nodes (22): _clamp_score(), parse_score_response(), Parse structured LLM responses into score dicts.  The LLM providers return the *, Coerce a raw score value to a valid 0-100 float., Parse LLM output into a validated, clamped ScoreResult.      Args:         raw:, Run a single LLM pass scoring the resume across all four dimensions., AnalysisStatus, AnalysisResponse (+14 more)

### Community 3 - "Resume Upload & Schema API"
Cohesion: 0.08
Nodes (18): Upload a resume file (PDF, DOC, DOCX)., upload_resume(), BaseModel, ResumeResponse, isoformat(), UTC datetime helpers., utcnow(), is_allowed_file() (+10 more)

### Community 4 - "Frontend Dependencies"
Cohesion: 0.06
Nodes (31): dependencies, react, react-dom, tailwindcss, @tailwindcss/vite, devDependencies, oxlint, @types/node (+23 more)

### Community 5 - "Auth & Security Utilities"
Cohesion: 0.09
Nodes (20): AsyncClient, hash_password(), Password security utilities (JWT removed — app is anonymous)., verify_password(), client(), db_engine(), db_session(), event_loop() (+12 more)

### Community 6 - "Frontend Internationalization"
Cohesion: 0.11
Nodes (27): Axios, Farsi (Vazirmatn) UI Support, Frontend HTML Entry Point, Farsi Language Support, Rationale: Font Role Assignment (Inter body, Sora display, Vazirmatn Farsi), Frontend index.html, Inter Font (body), Sora Font (display) (+19 more)

### Community 7 - "TypeScript App Config"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 8 - "Database Engine & Session"
Cohesion: 0.11
Nodes (18): close_db(), get_database(), get_db(), init_database(), init_db(), AsyncSession, Database configuration: async engine, session factory, lifecycle helpers., Dispose of the engine and all connections. (+10 more)

### Community 9 - "Cover Letter Generation"
Cohesion: 0.14
Nodes (20): Cover Letter Generation Prompt, Cover Letter Body (output field), Job Description Input (cover letter prompt), Resume Input (cover letter prompt), Cover Letter Subject (output field), Rationale: Tailored Cover Letter Generation, Grammar & Style Prompt, Grammar Score (0-100) (+12 more)

### Community 10 - "Node TSConfig"
Cohesion: 0.10
Nodes (19): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+11 more)

### Community 11 - "Analysis Results UI"
Cohesion: 0.16
Nodes (15): AnalysisResults(), AnalysisResultsProps, ScoreData, ScoreGauge(), ScoreGaugeProps, BAND_FILL, easeOutCubic(), getBandKey() (+7 more)

### Community 12 - "Standard Section Components"
Cohesion: 0.14
Nodes (13): Criterion, Standard, StandardSection(), Badge(), BadgeProps, BadgeTone, TONES, ProgressBar() (+5 more)

### Community 13 - "Analysis Domain & Scoring Service"
Cohesion: 0.18
Nodes (11): ResumeScorer, get_analysis_service(), Analysis, Analysis model — includes flat score columns for MVP., AnalysisRepository, AnalysisService, UUID, Analysis service — orchestrates the analysis workflow. (+3 more)

### Community 14 - "Exception Handling"
Cohesion: 0.18
Nodes (11): app_exception_handler(), AppException, ConflictException, ForbiddenException, NotFoundException, Exception, Request, Custom exception classes and FastAPI exception handlers. (+3 more)

### Community 15 - "Landing & Footer Components"
Cohesion: 0.19
Nodes (13): HowItWorks(), STEPS, Footer(), SOCIALS, Header(), Icon(), IconName, IconProps (+5 more)

### Community 16 - "Alembic Migrations"
Cohesion: 0.15
Nodes (11): Alembic, do_run_migrations(), Alembic async migration environment., Run migrations in 'offline' mode (emit SQL without connecting)., Configure context and run migrations on a live connection., Create an async engine and run migrations online., Run migrations in 'online' mode., run_async_migrations() (+3 more)

### Community 17 - "AI Provider Implementations"
Cohesion: 0.16
Nodes (7): ClaudeProvider, GeminiProvider, OpenAIProvider, OpenAI / OpenRouter-compatible provider., create_scorer(), get_llm_provider(), Standalone factory for ResumeScorer (usable outside FastAPI DI, e.g. Celery).

### Community 18 - "Rate Limiting Middleware"
Cohesion: 0.18
Nodes (9): BaseHTTPMiddleware, Request, RateLimitMiddleware, Redis-backed sliding-window rate limiter middleware., Sliding-window rate limiter using Redis.      Falls back to a simple in-memory c, Sliding-window counter using Redis sorted sets., In-memory sliding-window fallback., RequestResponseEndpoint (+1 more)

### Community 19 - "Base LLM Provider"
Cohesion: 0.20
Nodes (7): ABC, BaseLLMProvider, Abstract base for LLM providers., Send a prompt to the LLM and return the parsed response.          Args:, OpenRouterProvider, OpenRouter provider — routes to multiple models., OpenAI-compatible provider pointed at OpenRouter.      Does not call the parent

### Community 20 - "DBN Standard API"
Cohesion: 0.20
Nodes (8): download_standard(), get_active_standard(), DBN Standard (scoring rubric) routes., Return the currently active DBN scoring standard., Download the active DBN Standard as a markdown template., get_scoring_service(), Scoring service — encapsulates DBN Standard interactions., ScoringService

### Community 21 - "Base Repository"
Cohesion: 0.25
Nodes (5): BaseRepository, AsyncSession, UUID, Generic CRUD base repository., T

### Community 22 - "Docker Compose Services"
Cohesion: 0.40
Nodes (11): API Service (backend compose), Celery Beat Service (backend compose), Celery Worker Service (backend compose), PostgreSQL Database Service (backend compose), Redis Service (backend compose), API Service (compose), Celery Beat Service (compose), Celery Worker Service (compose) (+3 more)

### Community 23 - "Upload & CTA Components"
Cohesion: 0.22
Nodes (9): ALLOWED, UploadSection(), UploadSectionProps, Button(), ButtonProps, ButtonSize, ButtonVariant, SIZES (+1 more)

### Community 24 - "DBN Standard Repository"
Cohesion: 0.24
Nodes (5): get_standard_service(), DBNStandardRepository, DBN Standard repository., DBNStandardService, DBN Standard service.

### Community 25 - "Language Context (i18n)"
Cohesion: 0.27
Nodes (8): getNestedValue(), LanguageContext, LanguageContextValue, LanguageProvider(), Locale, translations, TranslationValue, TranslationKey

### Community 26 - "Frontend Type Definitions"
Cohesion: 0.20
Nodes (6): AnalysisResponse, AnalysisStatus, CriterionResponse, StandardResponse, ResumeResponse, ResumeStatus

### Community 27 - "AI Provider Modules"
Cohesion: 0.25
Nodes (6): Claude / Anthropic provider., Gemini (Google AI) provider — free tier via google-generativeai SDK., # NOTE: `google.generativeai` (deprecated) rejects pydantic schemas, configure_logging(), Centralized logging configuration., Call once during application startup.

### Community 28 - "Analysis API Endpoints"
Cohesion: 0.25
Nodes (6): get_analysis(), UUID, Analysis retrieval routes., Get the analysis results for a given analysis ID.      The path param is declare, API v1 router — aggregates all endpoint modules., Map the DB `feedback_json` column to the `feedback` field.

### Community 29 - "Standard Create Schema"
Cohesion: 0.31
Nodes (8): create_standard(), Create a new DBN scoring standard., CriterionCreate, CriterionResponse, BaseModel, DBN Standard schemas., StandardCreate, StandardResponse

### Community 30 - "Resumes API Endpoints"
Cohesion: 0.28
Nodes (8): analyze_resume(), delete_resume(), list_resumes(), UUID, Resume upload, listing, deletion, and analysis trigger., List all uploaded resumes., Delete a resume by ID., Trigger a new analysis for a resume.      In the MVP the scoring runs inline (Ce

### Community 31 - "App Entry & Lifespan"
Cohesion: 0.33
Nodes (6): create_app(), lifespan(), FastAPI application factory., configure_cors(), CORS middleware configuration., FastAPI

### Community 32 - "Lint Rules (oxlint)"
Cohesion: 0.22
Nodes (8): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema, oxc, typescript, warn

### Community 33 - "App Root & Theme Context"
Cohesion: 0.36
Nodes (4): ThemeContext, ThemeContextValue, ThemeProvider(), react

### Community 34 - "React Brand Assets"
Cohesion: 0.29
Nodes (7): Frontend Application (React SPA), React Brand Color #00D8FF, React Framework (UI Library), Frontend Stack (React), React Logo, React Logo SVG Asset (Atom Symbol), Iconify Logos Icon Set

### Community 35 - "Social Icon Set"
Cohesion: 0.43
Nodes (7): Icon Sprite (SVG Symbols), Bluesky Icon Symbol, Discord Icon Symbol, Documentation Icon Symbol, GitHub Icon Symbol, Social (Share) Icon Symbol, X (Twitter) Icon Symbol

### Community 36 - "SVG Icon Sprite"
Cohesion: 0.29
Nodes (7): bluesky-icon (Bluesky social logo), discord-icon (Discord social logo), documentation-icon (file/document glyph), github-icon (GitHub logo), icons.svg SVG sprite sheet, social-icon (user/social share glyph), x-icon (X / Twitter logo)

### Community 37 - "i18n Type Generation"
Cohesion: 0.29
Nodes (5): body, en, here, keys, src

### Community 38 - "Gemini Resume Mockup"
Cohesion: 0.29
Nodes (7): Sample Resume Document Content, Education Section, Work Experience Section, Resume Header (Name and Contact Info), Gemini Generated Resume Sample Image, Resume Reviewer Pipeline Input, Skills Section

### Community 39 - "Resume Screenshot Mockup"
Cohesion: 0.29
Nodes (7): Resume Document Content, Education Section, Work Experience Section, Resume Header (Name and Contact Info), Resume Screenshot Image, Skills Section, Resume Reviewer Pipeline Input

### Community 40 - "Settings & Configuration"
Cohesion: 0.33
Nodes (4): Path, Application configuration via Pydantic Settings., Settings, BaseSettings

### Community 41 - "Dependency Injection"
Cohesion: 0.33
Nodes (5): get_analysis_repo(), get_resume_repo(), get_scorer(), get_standard_repo(), Global dependency injection.

### Community 42 - "Request Logging Middleware"
Cohesion: 0.33
Nodes (4): BaseHTTPMiddleware, Request, Structured request/response logging middleware., RequestLoggingMiddleware

### Community 43 - "Hero Marketing Banner"
Cohesion: 0.33
Nodes (6): Resume reviewer brand promotional messaging, Call-to-action marketing element, Hero marketing banner (landing page, Resume Reviewer marketing hero image asset, Illustrative product UI/dashboard concept, Purple/lilac hero color scheme

### Community 44 - "Common Schemas"
Cohesion: 0.50
Nodes (4): ErrorResponse, PaginatedResponse, BaseModel, Shared response schemas.

### Community 45 - "PDF Text Extraction"
Cohesion: 0.40
Nodes (4): extract_text_from_pdf(), Path, PDF text extraction utilities using PyMuPDF (fitz)., Extract plain text from a PDF file.      Args:         path: Path to the PDF fil

### Community 46 - "Favicon & Brand Mark"
Cohesion: 0.50
Nodes (5): Resume Reviewer Favicon, Lightning Bolt Logo Mark, SaaS Web App Brand Identity, Purple Gradient Brand Palette, Resume Reviewer SaaS Platform

### Community 47 - "Hero Brand Theme"
Cohesion: 0.60
Nodes (5): Hero Brand Illustration (hero.png), Brand Violet-Indigo Palette, Decorative Concentric Diamond / Gem Outline, Solid Inverted-Pyramid Gradient Core (funnel motif), Landing Hero Section (UploadSection area)

### Community 48 - "Gemini Marketing Asset"
Cohesion: 0.50
Nodes (5): AI-generated digital illustration, Gemini-generated image asset (Resume Reviewer images folder), Marketing / branding / hero visual for Resume Reviewer SaaS platform, Resume Reviewer project, Depicted visual subject (document/resume + AI theme, per context)

### Community 49 - "Resume Scorer"
Cohesion: 0.50
Nodes (3): _load_prompt(), Orchestrates resume scoring using LLM providers and parsers., Load a prompt template from the prompts directory.      Uses plain string replac

### Community 50 - "Celery Analysis Worker"
Cohesion: 0.50
Nodes (3): analyze_resume(), Resume analysis Celery task — runs LLM scoring in the background., Run full resume analysis in the background.      1. Load analysis + resume from

### Community 51 - "Logo Brand Elements"
Cohesion: 0.83
Nodes (4): DBN Brand Logo, DBN Wordmark Monogram, Monochrome Brand Identity, Resume Scoring Visual Metaphor

### Community 53 - "Logo Identity"
Cohesion: 0.67
Nodes (3): Logo image asset (logo.jpg) for the Resume Reviewer SaaS application, Resume Reviewer brand mark (simple graphical emblem, monochrome, low visual detail), Identity link: logo represents the Resume Reviewer AI resume-analysis SaaS product

### Community 54 - "Vite Build Assets"
Cohesion: 0.67
Nodes (3): Vite Build Tool, Vite Logo, Vite Build Tool Brand

## Ambiguous Edges - Review These
- `Hero Brand Illustration (hero.png)` → `Landing Hero Section (UploadSection area)`  [AMBIGUOUS]
  frontend/src/assets/hero.png · relation: conceptually_related_to

## Knowledge Gaps
- **169 isolated node(s):** `dbn-resume-reviewer`, `$schema`, `typescript`, `oxc`, `react/rules-of-hooks` (+164 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Hero Brand Illustration (hero.png)` and `Landing Hero Section (UploadSection area)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `DBN Resume Reviewer` connect `ATS Scoring System` to `Docker Compose Services`, `Frontend Internationalization`?**
  _High betweenness centrality (0.168) - this node is a cross-community bridge._
- **Why does `FastAPI Backend` connect `ATS Scoring System` to `Alembic Migrations`, `Core Domain Constants & Enums`, `Auth & Security Utilities`?**
  _High betweenness centrality (0.168) - this node is a cross-community bridge._
- **Why does `SQLAlchemy 2.0 async` connect `Core Domain Constants & Enums` to `ATS Scoring System`, `Database Engine & Session`, `Analysis Domain & Scoring Service`, `Alembic Migrations`, `Base Repository`, `DBN Standard Repository`?**
  _High betweenness centrality (0.151) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `Database` (e.g. with `UserRole` and `DBNStandard`) actually correct?**
  _`Database` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `User` (e.g. with `Database` and `.init_db()`) actually correct?**
  _`User` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `dbn-resume-reviewer`, `$schema`, `typescript` to the rest of the system?**
  _169 weakly-connected nodes found - possible documentation gaps or missing edges._