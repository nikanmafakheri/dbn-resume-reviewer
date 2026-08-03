# Graph Report - /home/nikan/Documents/resume-reviewer  (2026-08-03)

## Corpus Check
- 134 files · ~143,809 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 828 nodes · 1201 edges · 87 communities (55 shown, 32 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 203 edges (avg confidence: 0.74)
- Token cost: 2,500 input · 1,981 output

## Community Hubs (Navigation)
- Score Parser & Parsing
- Analysis Models & Results
- Database Engine Setup
- LLM Providers & Abstraction
- ATS & Prompt Logic
- Error Handling & Exceptions
- Resume Upload & File Handling
- DB Session Management
- Frontend Build & Dependencies
- Docker Compose Services
- Analysis Schemas & Contracts
- Security & Test Utilities
- Frontend TS Config
- Landing Page UI
- Analysis Results UI
- Node TS Config
- Alembic Migrations
- Standard Template UI
- DBN Standard Routes
- Upload & Buttons UI
- Repository Layer
- Deployment Services
- Language & i18n Context
- Lint Config
- Icon Sprites
- Community 25
- Community 26
- Community 27
- Community 28
- Community 29
- Community 30
- Community 31
- Community 32
- Community 33
- Community 34
- Community 35
- Community 36
- Community 37
- Community 38
- Community 40
- Community 41
- Community 42
- Community 43
- Community 44
- Community 45
- Community 46
- Community 47
- Community 48
- Community 64
- Community 65
- Community 66
- Community 67
- Community 68
- Community 69
- Community 70
- Community 71
- Community 72
- Community 73
- Community 74
- Community 75
- Community 76
- Community 78
- Community 79
- Community 80
- Community 81
- Community 82
- Community 83
- Community 84
- Community 85
- Community 86

## God Nodes (most connected - your core abstractions)
1. `ScoreParseError` - 24 edges
2. `parse_score_response()` - 24 edges
3. `ResumeScorer` - 20 edges
4. `compilerOptions` - 18 edges
5. `Database` - 17 edges
6. `TestScoreParser` - 16 edges
7. `compilerOptions` - 15 edges
8. `SQLAlchemy 2.0 async` - 15 edges
9. `AnalysisService` - 14 edges
10. `User` - 13 edges

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
- **AI Provider Set** — gemini, openai, claude_ai, openrouter [EXTRACTED 1.00]
- **Resume Scoring Dimensions** — ats_compatibility, grammar_style, recruiter_appeal, overall_score [EXTRACTED 1.00]
- **Full-Stack Architecture** — backend_stack, frontend_stack, postgres_db, redis_cache [EXTRACTED 0.95]
- **AI Provider Ecosystem** — gemini, openai, claude_ai, openrouter [EXTRACTED 1.00]
- **Resume Scoring Dimensions** — ats_compatibility, grammar_style, recruiter_appeal, overall_score [EXTRACTED 1.00]
- **Celery Task Infrastructure** — api_service, celery_worker_service, celery_beat_service, redis_cache [EXTRACTED 1.00]
- **Backend Compose Services** — backend_docker_compose_api, backend_docker_compose_celery_worker, backend_docker_compose_celery_beat, backend_docker_compose_db, backend_docker_compose_redis [EXTRACTED 1.00]
- **Full-Stack Compose Services (top-level)** — docker_compose_api, docker_compose_celery_worker, docker_compose_celery_beat, docker_compose_db, docker_compose_redis [EXTRACTED 1.00]
- **Frontend Technology Stack** — frontend_readme_react, frontend_readme_typescript, frontend_readme_vite [INFERRED 0.95]
- **Favicon Brand Fragment** — frontend_public_favicon, frontend_public_favicon_bolt_mark, frontend_public_favicon_purple_palette, frontend_public_favicon_brand_purpose [INFERRED 0.85]
- **Social / Brand Icon Set** — frontend_public_icons_bluesky_icon, frontend_public_icons_discord_icon, frontend_public_icons_github_icon, frontend_public_icons_social_icon, frontend_public_icons_x_icon, frontend_public_icons_documentation_icon [EXTRACTED 1.00]
- **DBN Resume Reviewer Brand Identity** — frontend_public_logo, frontend_public_logo_dbn, frontend_public_logo_scoring, frontend_public_logo_monochrome [INFERRED 0.85]
- **Hero Brand Visual Identity** — frontend_src_assets_hero, frontend_src_assets_hero_gem_ring, frontend_src_assets_hero_gradient_funnel, frontend_src_assets_hero_brand_violet [INFERRED 0.85]
- **React Logo Rendered as SVG** — frontend_src_assets_react_svg, frontend_src_assets_react_framework, iconify_logos, frontend_src_assets_react_brand_color [EXTRACTED 0.90]
- **Resume Composed of Standard Sections** — images_resume_header, images_resume_experience, images_resume_education, images_resume_skills [INFERRED 0.85]
- **Sample Resume Composed of Standard Sections** — images_gemini_generated_image_1tjqx1tjqx1tjqx1_header, images_gemini_generated_image_1tjqx1tjqx1tjqx1_experience, images_gemini_generated_image_1tjqx1tjqx1tjqx1_education, images_gemini_generated_image_1tjqx1tjqx1tjqx1_skills [INFERRED 0.85]
- **Shared ATS Evaluation Rubric** — backend_app_ai_prompts_ats, backend_app_ai_prompts_resume_analysis, backend_app_ai_prompts_ats_keyword_coverage [INFERRED 0.95]
- **Writing Quality Rubric Cluster** — backend_app_ai_prompts_grammar, content_quality_dimension, error_free_writing [INFERRED 0.85]

## Communities (87 total, 32 thin omitted)

### Community 0 - "Score Parser & Parsing"
Cohesion: 0.06
Nodes (35): _ensure_json(), _parse_dimension(), _parse_float(), parse_score_response(), _parse_string_list(), ScoreResult, Strict parser for LLM scoring responses.  The scoring pipeline is deterministic, Parse and strictly validate an LLM scoring response.      Args:         raw: Raw (+27 more)

### Community 1 - "Analysis Models & Results"
Cohesion: 0.05
Nodes (44): get_analysis(), UUID, Analysis retrieval routes., Get the analysis results for a given analysis ID.      The path param is declare, analyze_resume(), delete_resume(), list_resumes(), UUID (+36 more)

### Community 2 - "Database Engine Setup"
Cohesion: 0.06
Nodes (28): Database, Manages the async SQLAlchemy engine and session factory., Create async SQLAlchemy engine with sensible defaults., Create tables (dev bootstrap) and seed defaults, idempotently.          In produ, get_scoring_service(), get_standard_service(), Analysis model — flat legacy score columns plus nested result JSON.  New-style a, Base (+20 more)

### Community 3 - "LLM Providers & Abstraction"
Cohesion: 0.06
Nodes (24): ABC, BaseLLMProvider, Abstract base for LLM providers., Send a prompt to the LLM and return the parsed response.          Args:, ClaudeProvider, Claude / Anthropic provider., GeminiProvider, Gemini (Google AI) provider — free tier via google-generativeai SDK. (+16 more)

### Community 4 - "ATS & Prompt Logic"
Cohesion: 0.08
Nodes (41): Axios, ATS Compatibility Analysis Prompt, ATS Keyword Coverage, ATS 0-100 Scoring Guide, Cover Letter Generation Prompt, Grammar & Style Analysis Prompt, DBN Resume Evaluation System Prompt, Content Quality Dimension (+33 more)

### Community 5 - "Error Handling & Exceptions"
Cohesion: 0.07
Nodes (26): app_exception_handler(), AppException, ConflictException, ForbiddenException, NotFoundException, Exception, Request, Custom exception classes and FastAPI exception handlers. (+18 more)

### Community 6 - "Resume Upload & File Handling"
Cohesion: 0.07
Nodes (26): Upload a resume file (PDF, DOC, DOCX)., upload_resume(), is_allowed_file(), is_valid_file_size(), File upload validation and security utilities., Sanitize filename for safe storage/display., Check if file extension is allowed., Check if file size is within limits. (+18 more)

### Community 7 - "DB Session Management"
Cohesion: 0.08
Nodes (25): close_db(), get_database(), get_db(), init_database(), init_db(), AsyncSession, Database configuration: async engine, session factory, lifecycle helpers., Dispose of the engine and all connections. (+17 more)

### Community 8 - "Frontend Build & Dependencies"
Cohesion: 0.06
Nodes (31): dependencies, react, react-dom, tailwindcss, @tailwindcss/vite, devDependencies, oxlint, @types/node (+23 more)

### Community 9 - "Docker Compose Services"
Cohesion: 0.11
Nodes (30): API Service, ATS Compatibility, Celery app configuration., Backend docker-compose.yml, Backend Stack (FastAPI), Celery, Celery Beat Scheduler, Celery Worker Service (+22 more)

### Community 10 - "Analysis Schemas & Contracts"
Cohesion: 0.09
Nodes (24): AnalysisResponse, Confidence, DimensionScore, BaseModel, Analysis schemas — strict JSON contract for the DBN scoring pipeline.  Every sco, One dimension's score plus the evidence that justifies it., Structural confidence — how much of the requested schema validated., Full validated result of a resume evaluation.      ``overall`` is recomputed by (+16 more)

### Community 11 - "Security & Test Utilities"
Cohesion: 0.10
Nodes (18): AsyncClient, hash_password(), Password security utilities (JWT removed — app is anonymous)., verify_password(), client(), db_engine(), db_session(), event_loop() (+10 more)

### Community 12 - "Frontend TS Config"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 13 - "Landing Page UI"
Cohesion: 0.16
Nodes (16): HowItWorks(), STEPS, Footer(), SOCIALS, Header(), Icon(), IconName, IconProps (+8 more)

### Community 14 - "Analysis Results UI"
Cohesion: 0.15
Nodes (15): AnalysisResults(), AnalysisResultsProps, ScoreData, ScoreGauge(), ScoreGaugeProps, BAND_FILL, easeOutCubic(), getBandKey() (+7 more)

### Community 15 - "Node TS Config"
Cohesion: 0.10
Nodes (19): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+11 more)

### Community 16 - "Alembic Migrations"
Cohesion: 0.12
Nodes (11): Alembic, do_run_migrations(), Alembic async migration environment., Run migrations in 'offline' mode (emit SQL without connecting)., Configure context and run migrations on a live connection., Create an async engine and run migrations online., Run migrations in 'online' mode., run_async_migrations() (+3 more)

### Community 17 - "Standard Template UI"
Cohesion: 0.14
Nodes (13): Criterion, Standard, StandardSection(), Badge(), BadgeProps, BadgeTone, TONES, ProgressBar() (+5 more)

### Community 18 - "DBN Standard Routes"
Cohesion: 0.15
Nodes (14): create_standard(), download_standard(), get_active_standard(), DBN Standard (scoring rubric) routes., Return the currently active DBN scoring standard., Download the active DBN Standard as a markdown template., Create a new DBN scoring standard., API v1 router — aggregates all endpoint modules. (+6 more)

### Community 19 - "Upload & Buttons UI"
Cohesion: 0.19
Nodes (10): ALLOWED, UploadSection(), UploadSectionProps, Button(), ButtonProps, ButtonSize, ButtonVariant, SIZES (+2 more)

### Community 20 - "Repository Layer"
Cohesion: 0.25
Nodes (5): BaseRepository, AsyncSession, UUID, Generic CRUD base repository., T

### Community 21 - "Deployment Services"
Cohesion: 0.40
Nodes (11): API Service (backend compose), Celery Beat Service (backend compose), Celery Worker Service (backend compose), PostgreSQL Database Service (backend compose), Redis Service (backend compose), API Service (compose), Celery Beat Service (compose), Celery Worker Service (compose) (+3 more)

### Community 22 - "Language & i18n Context"
Cohesion: 0.27
Nodes (8): getNestedValue(), LanguageContext, LanguageContextValue, LanguageProvider(), Locale, translations, TranslationValue, TranslationKey

### Community 23 - "Lint Config"
Cohesion: 0.22
Nodes (8): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema, oxc, typescript, warn

### Community 24 - "Icon Sprites"
Cohesion: 0.43
Nodes (7): Icon Sprite (SVG Symbols), Bluesky Icon Symbol, Discord Icon Symbol, Documentation Icon Symbol, GitHub Icon Symbol, Social (Share) Icon Symbol, X (Twitter) Icon Symbol

### Community 25 - "Community 25"
Cohesion: 0.29
Nodes (5): body, en, here, keys, src

### Community 26 - "Community 26"
Cohesion: 0.29
Nodes (6): AnalysisResponse, AnalysisStatus, Confidence, DimensionScore, ScoreDimensionKey, ScoreResult

### Community 27 - "Community 27"
Cohesion: 0.29
Nodes (4): CriterionResponse, StandardResponse, ResumeResponse, ResumeStatus

### Community 28 - "Community 28"
Cohesion: 0.29
Nodes (7): Sample Resume Document Content, Education Section, Work Experience Section, Resume Header (Name and Contact Info), Gemini Generated Resume Sample Image, Resume Reviewer Pipeline Input, Skills Section

### Community 29 - "Community 29"
Cohesion: 0.29
Nodes (7): Resume Document Content, Education Section, Work Experience Section, Resume Header (Name and Contact Info), Resume Screenshot Image, Skills Section, Resume Reviewer Pipeline Input

### Community 30 - "Community 30"
Cohesion: 0.33
Nodes (4): Path, Application configuration via Pydantic Settings., Settings, BaseSettings

### Community 31 - "Community 31"
Cohesion: 0.33
Nodes (5): band(), classified(), DBN Resume evaluation rubric — the single source of truth for scoring.  Every sc, Map a 0-100 score to a display band key., Return ``"yes"/"no"`` for a boolean predicate.      Used to keep the LLM output

### Community 32 - "Community 32"
Cohesion: 0.33
Nodes (6): Resume reviewer brand promotional messaging, Call-to-action marketing element, Hero marketing banner (landing page, Resume Reviewer marketing hero image asset, Illustrative product UI/dashboard concept, Purple/lilac hero color scheme

### Community 33 - "Community 33"
Cohesion: 0.50
Nodes (4): ErrorResponse, PaginatedResponse, BaseModel, Shared response schemas.

### Community 34 - "Community 34"
Cohesion: 0.40
Nodes (5): Frontend Application (React SPA), React Brand Color #00D8FF, React Framework (UI Library), React Logo SVG Asset (Atom Symbol), Iconify Logos Icon Set

### Community 35 - "Community 35"
Cohesion: 0.50
Nodes (5): Resume Reviewer Favicon, Lightning Bolt Logo Mark, SaaS Web App Brand Identity, Purple Gradient Brand Palette, Resume Reviewer SaaS Platform

### Community 36 - "Community 36"
Cohesion: 0.60
Nodes (5): Hero Brand Illustration (hero.png), Brand Violet-Indigo Palette, Decorative Concentric Diamond / Gem Outline, Solid Inverted-Pyramid Gradient Core (funnel motif), Landing Hero Section (UploadSection area)

### Community 37 - "Community 37"
Cohesion: 0.83
Nodes (4): DBN Brand Logo, DBN Wordmark Monogram, Monochrome Brand Identity, Resume Scoring Visual Metaphor

## Ambiguous Edges - Review These
- `Hero Brand Illustration (hero.png)` → `Landing Hero Section (UploadSection area)`  [AMBIGUOUS]
  frontend/src/assets/hero.png · relation: conceptually_related_to

## Knowledge Gaps
- **172 isolated node(s):** `dbn-resume-reviewer`, `$schema`, `typescript`, `oxc`, `react/rules-of-hooks` (+167 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **32 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Hero Brand Illustration (hero.png)` and `Landing Hero Section (UploadSection area)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `FastAPI Backend` connect `Docker Compose Services` to `Alembic Migrations`, `Score Parser & Parsing`, `Database Engine Setup`?**
  _High betweenness centrality (0.154) - this node is a cross-community bridge._
- **Why does `DBN Resume Reviewer` connect `Docker Compose Services` to `ATS & Prompt Logic`, `Deployment Services`?**
  _High betweenness centrality (0.146) - this node is a cross-community bridge._
- **Why does `SQLAlchemy 2.0 async` connect `Database Engine Setup` to `Alembic Migrations`, `Docker Compose Services`, `Repository Layer`, `DB Session Management`?**
  _High betweenness centrality (0.125) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `ScoreParseError` (e.g. with `ResumeScorer` and `._verify_overall()`) actually correct?**
  _`ScoreParseError` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `parse_score_response()` (e.g. with `weighted_overall()` and `Confidence`) actually correct?**
  _`parse_score_response()` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `ResumeScorer` (e.g. with `ScoreParseError` and `BaseLLMProvider`) actually correct?**
  _`ResumeScorer` has 9 INFERRED edges - model-reasoned connections that need verification._