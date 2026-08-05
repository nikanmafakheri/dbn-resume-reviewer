# Graph Report - .  (2026-08-05)

## Corpus Check
- 137 files · ~147,602 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 852 nodes · 1212 edges · 101 communities (64 shown, 37 thin omitted)
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 221 edges (avg confidence: 0.73)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Core Constants & Enums
- DB Engine & Standard Routes
- Analysis API Endpoints
- Score Parser & Validation
- Scorer Timeout & Retry Logic
- Frontend Build & Dependencies
- Resume Scoring Prompt & Dimensions
- Alembic Migrations
- Security & Test Setup
- Frontend tsconfig (app)
- DB Session Management
- Resume Schemas & Utils
- Upload & File Validation
- Frontend tsconfig (node)
- Analysis Results UI
- Standard Template UI
- Error Handling & Exceptions
- Landing Page & Footer UI
- Analysis Service & Repository
- Rate Limit Middleware
- Analysis Types & Contracts
- LLM Provider Abstraction
- AI Provider Implementations
- Base Repository Layer
- Docker Compose Services
- Upload Section UI
- App Shell & Theme Context
- Language & i18n Context
- Timeout & Analyze Route Flow
- Gemini/Claude Provider Classes
- DBN Standard CRUD & Schemas
- Quota UX Plan (plan.md)
- Frontend Lint Config
- Rate-Limit Error Classification
- Config Settings
- PDF Text Extraction
- DB Index Tests
- Public Icon Set
- i18n Type Generation
- Gemini Sample Images
- Resume Example Images
- Hero Assets & CTA
- Common Schemas
- App Assets & React Logo
- Favicon & Brand Mark
- Hero Visual Assets
- Logo & Scoring Mark
- Test Factories
- tsconfig Root
- AI Package Init
- Models Package Init
- Middleware Package Init
- Utils Package Init
- Celery Worker Config
- Workers Package Init
- Verify Stack Script
- Brand & Favicon Marks
- Vite Logo Assets
- File Type Constants
- Backend Stack
- Claude MD
- Bluesky Icon
- Discord Icon
- Documentation Icon
- Github Icon
- Icons SVG Sprite
- Social Icons
- X Icon
- Logo Asset
- Logo Brand
- Logo Identity
- React Frontend Stack
- React Logo
- Vite Build Tool
- ChatGPT Sample Image
- ChatGPT UI Mockup
- Gemini AI Generated
- Gemini Asset
- Gemini Marketing Asset
- Gemini Project Image
- Gemini Visual Content
- Photo Asset
- DBN Resume Reviewer Package
- React Frontend

## God Nodes (most connected - your core abstractions)
1. `ScoreParseError` - 24 edges
2. `parse_score_response()` - 24 edges
3. `ResumeScorer` - 22 edges
4. `compilerOptions` - 18 edges
5. `Database` - 17 edges
6. `TestScoreParser` - 16 edges
7. `AnalysisService` - 15 edges
8. `FakeScorer` - 15 edges
9. `compilerOptions` - 15 edges
10. `ProviderRateLimitError` - 14 edges

## Surprising Connections (you probably didn't know these)
- `Frontend README (Vite template)` --references--> `Frontend Stack (React 19)`  [INFERRED]
  frontend/README.md → CLAUDE.md
- `Backend CI Job` --references--> `DBN Resume Reviewer`  [INFERRED]
  .github/workflows/ci.yml → README.md
- `Frontend CI Job` --references--> `DBN Resume Reviewer`  [INFERRED]
  .github/workflows/ci.yml → README.md
- `Postgres Service` --references--> `DBN Resume Reviewer`  [INFERRED]
  docker-compose.yml → README.md
- `Frontend index.html` --conceptually_related_to--> `vite`  [INFERRED]
  frontend/index.html → frontend/package.json

## Import Cycles
- 1-file cycle: `backend/app/workers/celery.py -> backend/app/workers/celery.py`

## Hyperedges (group relationships)
- **AI Provider Set** — backend_app_ai_providers_gemini, backend_app_ai_providers_openai, backend_app_ai_providers_openrouter [EXTRACTED 1.00]
- **Frontend Technology Stack** — frontend_readme_react, frontend_readme_typescript, frontend_readme_vite [INFERRED 0.95]
- **Favicon Brand Fragment** — frontend_public_favicon, frontend_public_favicon_bolt_mark, frontend_public_favicon_purple_palette, frontend_public_favicon_brand_purpose [INFERRED 0.85]
- **Social / Brand Icon Set** — frontend_public_icons_bluesky_icon, frontend_public_icons_discord_icon, frontend_public_icons_github_icon, frontend_public_icons_social_icon, frontend_public_icons_x_icon, frontend_public_icons_documentation_icon [EXTRACTED 1.00]
- **DBN Resume Reviewer Brand Identity** — frontend_public_logo, frontend_public_logo_dbn, frontend_public_logo_scoring, frontend_public_logo_monochrome [INFERRED 0.85]
- **Hero Brand Visual Identity** — frontend_src_assets_hero, frontend_src_assets_hero_gem_ring, frontend_src_assets_hero_gradient_funnel, frontend_src_assets_hero_brand_violet [INFERRED 0.85]
- **React Logo Rendered as SVG** — frontend_src_assets_react_svg, frontend_src_assets_react_framework, iconify_logos, frontend_src_assets_react_brand_color [EXTRACTED 0.90]
- **Resume Composed of Standard Sections** — images_resume_header, images_resume_experience, images_resume_education, images_resume_skills [INFERRED 0.85]
- **Sample Resume Composed of Standard Sections** — images_gemini_generated_image_1tjqx1tjqx1tjqx1_header, images_gemini_generated_image_1tjqx1tjqx1tjqx1_experience, images_gemini_generated_image_1tjqx1tjqx1tjqx1_education, images_gemini_generated_image_1tjqx1tjqx1tjqx1_skills [INFERRED 0.85]
- **Quota and Rate-Limit 429 Handling Flow** — claude_plan_quotaux, claude_plan_providerratelimiterror, claude_plan_errorcode, claude_plan_middleware429, claude_plan_isratelimiterror, claude_plan_waitretrycard, claude_plan_retrysemantics [EXTRACTED 1.00]
- **CI Pipeline** — github_workflows_ci_workflow, github_workflows_ci_backendjob, github_workflows_ci_frontendjob [EXTRACTED 0.95]
- **Background Task Queue** — docker_compose_apiservice, docker_compose_celeryworker, docker_compose_celerybeat, docker_compose_redisservice [INFERRED 0.75]
- **Full Stack Application** — docker_compose_apiservice, docker_compose_dbservice, docker_compose_redisservice [EXTRACTED 0.95]

## Communities (101 total, 37 thin omitted)

### Community 0 - "Core Constants & Enums"
Cohesion: 0.05
Nodes (48): AnalysisStatus, Application-wide constants and enums., ResumeStatus, UserRole, AnalysisResponse, Confidence, DimensionScore, BaseModel (+40 more)

### Community 1 - "DB Engine & Standard Routes"
Cohesion: 0.06
Nodes (31): get_active_standard(), Return the currently active DBN scoring standard., Database, Manages the async SQLAlchemy engine and session factory., Create async SQLAlchemy engine with sensible defaults., Create tables (dev bootstrap) and seed defaults, idempotently.          In produ, get_scoring_service(), get_standard_service() (+23 more)

### Community 2 - "Analysis API Endpoints"
Cohesion: 0.05
Nodes (37): get_analysis(), UUID, Analysis retrieval routes., Get the analysis results for a given analysis ID.      The path param is declare, download_template(), DBN Standard (scoring rubric) routes., Download the DBN Standard resume template as a .pptx file., delete_resume() (+29 more)

### Community 3 - "Score Parser & Validation"
Cohesion: 0.09
Nodes (25): _ensure_json(), _parse_dimension(), _parse_float(), parse_score_response(), _parse_string_list(), ScoreResult, Strict parser for LLM scoring responses.  The scoring pipeline is deterministic, Parse and strictly validate an LLM scoring response.      Args:         raw: Raw (+17 more)

### Community 4 - "Scorer Timeout & Retry Logic"
Cohesion: 0.11
Nodes (18): ProviderTimeoutError, Raised when a single LLM request exceeds its time budget.      Like :class:`Prov, _load_prompt(), ScoreResult, Orchestrates resume scoring using LLM providers and parsers.  Guarantees of this, Construct a corrective prompt embedding the exact parse error.          The orig, Human-readable description of the required JSON contract., Load a prompt template from the prompts directory.      Uses plain string replac (+10 more)

### Community 5 - "Frontend Build & Dependencies"
Cohesion: 0.06
Nodes (31): dependencies, react, react-dom, tailwindcss, @tailwindcss/vite, devDependencies, oxlint, @types/node (+23 more)

### Community 6 - "Resume Scoring Prompt & Dimensions"
Cohesion: 0.10
Nodes (30): DBN Resume Evaluation System Prompt, Content Quality Dimension, Programmatic Dimension-Weighted Scoring, Farsi (Vazirmatn) UI Support, Frontend HTML Entry Point, AI-Powered Resume Review and Scoring, DBN Resume Reviewer (app title), Farsi Language Support (+22 more)

### Community 7 - "Alembic Migrations"
Cohesion: 0.09
Nodes (13): Alembic, do_run_migrations(), _migration_url(), Alembic async migration environment., Resolve the migration target URL.      The app's settings read DATABASE_URL (env, Run migrations in 'offline' mode (emit SQL without connecting)., Configure context and run migrations on a live connection., Create an async engine and run migrations online. (+5 more)

### Community 8 - "Security & Test Setup"
Cohesion: 0.10
Nodes (18): AsyncClient, hash_password(), Password security utilities (JWT removed — app is anonymous)., verify_password(), client(), db_engine(), db_session(), event_loop() (+10 more)

### Community 9 - "Frontend tsconfig (app)"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 10 - "DB Session Management"
Cohesion: 0.11
Nodes (18): close_db(), get_database(), get_db(), init_database(), init_db(), AsyncSession, Database configuration: async engine, session factory, lifecycle helpers., Dispose of the engine and all connections. (+10 more)

### Community 11 - "Resume Schemas & Utils"
Cohesion: 0.12
Nodes (12): BaseModel, ResumeResponse, isoformat(), UTC datetime helpers., utcnow(), Custom Pydantic validators., validate_password(), Unit tests for utility functions. (+4 more)

### Community 12 - "Upload & File Validation"
Cohesion: 0.13
Nodes (15): Upload a resume file (PDF, DOC, DOCX)., upload_resume(), is_allowed_file(), is_valid_file_size(), File upload validation and security utilities., Sanitize filename for safe storage/display., Check if file extension is allowed., Check if file size is within limits. (+7 more)

### Community 13 - "Frontend tsconfig (node)"
Cohesion: 0.10
Nodes (19): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+11 more)

### Community 14 - "Analysis Results UI"
Cohesion: 0.15
Nodes (14): AnalysisResultsProps, ScoreData, ScoreGauge(), ScoreGaugeProps, BAND_FILL, easeOutCubic(), getBandKey(), getScoreBand() (+6 more)

### Community 15 - "Standard Template UI"
Cohesion: 0.14
Nodes (13): Criterion, Standard, StandardSection(), Badge(), BadgeProps, BadgeTone, TONES, ProgressBar() (+5 more)

### Community 16 - "Error Handling & Exceptions"
Cohesion: 0.18
Nodes (11): app_exception_handler(), AppException, ConflictException, ForbiddenException, NotFoundException, Exception, Request, Custom exception classes and FastAPI exception handlers. (+3 more)

### Community 17 - "Landing Page & Footer UI"
Cohesion: 0.19
Nodes (13): HowItWorks(), STEPS, Footer(), SOCIALS, Header(), Icon(), IconName, IconProps (+5 more)

### Community 18 - "Analysis Service & Repository"
Cohesion: 0.17
Nodes (10): get_analysis_service(), AnalysisRepository, AnalysisService, UUID, Analysis service — orchestrates the analysis workflow., analyze_resume(), Resume analysis Celery task — runs LLM scoring in the background., Run full resume analysis in the background.      1. Load analysis + resume from (+2 more)

### Community 19 - "Rate Limit Middleware"
Cohesion: 0.18
Nodes (9): BaseHTTPMiddleware, Request, RateLimitMiddleware, Redis-backed sliding-window rate limiter middleware., Sliding-window rate limiter using Redis.      Falls back to a simple in-memory c, Sliding-window counter using Redis sorted sets., In-memory sliding-window fallback., RequestResponseEndpoint (+1 more)

### Community 20 - "Analysis Types & Contracts"
Cohesion: 0.14
Nodes (10): AnalysisResponse, AnalysisStatus, Confidence, DimensionScore, ScoreDimensionKey, ScoreResult, CriterionResponse, StandardResponse (+2 more)

### Community 21 - "LLM Provider Abstraction"
Cohesion: 0.20
Nodes (7): ABC, BaseLLMProvider, Abstract base for LLM providers., Send a prompt to the LLM and return the parsed response.          Args:, OpenRouterProvider, OpenRouter provider — routes to multiple models., OpenAI-compatible provider pointed at OpenRouter.      Does not call the parent

### Community 22 - "AI Provider Implementations"
Cohesion: 0.20
Nodes (7): Claude / Anthropic provider., Gemini (Google AI) provider — free tier via google-generativeai SDK., # NOTE: `google.generativeai` (deprecated) rejects pydantic schemas, OpenAI / OpenRouter-compatible provider., configure_logging(), Centralized logging configuration., Call once during application startup.

### Community 23 - "Base Repository Layer"
Cohesion: 0.25
Nodes (5): BaseRepository, AsyncSession, UUID, Generic CRUD base repository., T

### Community 24 - "Docker Compose Services"
Cohesion: 0.22
Nodes (11): API Service, Celery Beat Service, Celery Worker Service, Postgres Service, Redis Service, Backend CI Job, Frontend CI Job, CI Workflow (+3 more)

### Community 25 - "Upload Section UI"
Cohesion: 0.22
Nodes (9): ALLOWED, UploadSection(), UploadSectionProps, Button(), ButtonProps, ButtonSize, ButtonVariant, SIZES (+1 more)

### Community 26 - "App Shell & Theme Context"
Cohesion: 0.31
Nodes (7): App(), AnalysisResults(), ThemeContext, ThemeContextValue, ThemeProvider(), isRateLimitError(), react

### Community 27 - "Language & i18n Context"
Cohesion: 0.27
Nodes (8): getNestedValue(), LanguageContext, LanguageContextValue, LanguageProvider(), Locale, translations, TranslationValue, TranslationKey

### Community 28 - "Timeout & Analyze Route Flow"
Cohesion: 0.22
Nodes (7): is_timeout_error(), Exception, True if ``exc`` (or its wrapped message) signals a request timeout.      Used al, analyze_resume(), Trigger a new analysis for a resume.      In the MVP the scoring runs inline (Ce, Called from Celery worker., Persist a validated ScoreResult into the Analysis row.          Mirrors the five

### Community 29 - "Gemini/Claude Provider Classes"
Cohesion: 0.28
Nodes (6): ClaudeProvider, GeminiProvider, OpenAIProvider, create_scorer(), get_llm_provider(), Standalone factory for ResumeScorer (usable outside FastAPI DI, e.g. Celery).

### Community 30 - "DBN Standard CRUD & Schemas"
Cohesion: 0.31
Nodes (8): create_standard(), Create a new DBN scoring standard., CriterionCreate, CriterionResponse, BaseModel, DBN Standard schemas., StandardCreate, StandardResponse

### Community 31 - "Quota UX Plan (plan.md)"
Cohesion: 0.22
Nodes (9): error_code Field, isRateLimitError Helper, Middleware 429 Rate-Limit, ProviderRateLimitError, Quota i18n Key Group, Quota Exhausted UX, Retry Semantics (Re-Post New Analysis), Wait & Retry Amber Card (+1 more)

### Community 32 - "Frontend Lint Config"
Cohesion: 0.22
Nodes (8): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema, oxc, typescript, warn

### Community 33 - "Rate-Limit Error Classification"
Cohesion: 0.43
Nodes (5): is_rate_limit_error(), ProviderRateLimitError, True if ``exc`` (or its wrapped message) signals quota/rate-limit.      Provider, Raised when the LLM provider is rate-limited or out of quota.      Distinguishes, RuntimeError

### Community 34 - "Config Settings"
Cohesion: 0.33
Nodes (4): Path, Application configuration via Pydantic Settings., Settings, BaseSettings

### Community 35 - "PDF Text Extraction"
Cohesion: 0.33
Nodes (6): extract_text_from_pdf(), Path, PDF text extraction utilities using PyMuPDF (fitz)., Extract plain text from a PDF file.      Args:         path: Path to the PDF fil, Validate PDF for security issues without extracting text.      Returns:, validate_pdf_security()

### Community 36 - "DB Index Tests"
Cohesion: 0.48
Nodes (6): Assert the production index set is present on ORM metadata.  These indexes are t, _table_index_columns(), test_analyses_fk_and_listing_indexes(), test_resumes_fk_and_listing_indexes(), test_standard_criteria_and_standards_fk_indexes(), test_users_role_index()

### Community 37 - "Public Icon Set"
Cohesion: 0.43
Nodes (7): Icon Sprite (SVG Symbols), Bluesky Icon Symbol, Discord Icon Symbol, Documentation Icon Symbol, GitHub Icon Symbol, Social (Share) Icon Symbol, X (Twitter) Icon Symbol

### Community 38 - "i18n Type Generation"
Cohesion: 0.29
Nodes (5): body, en, here, keys, src

### Community 39 - "Gemini Sample Images"
Cohesion: 0.29
Nodes (7): Sample Resume Document Content, Education Section, Work Experience Section, Resume Header (Name and Contact Info), Gemini Generated Resume Sample Image, Resume Reviewer Pipeline Input, Skills Section

### Community 40 - "Resume Example Images"
Cohesion: 0.29
Nodes (7): Resume Document Content, Education Section, Work Experience Section, Resume Header (Name and Contact Info), Resume Screenshot Image, Skills Section, Resume Reviewer Pipeline Input

### Community 41 - "Hero Assets & CTA"
Cohesion: 0.33
Nodes (6): Resume reviewer brand promotional messaging, Call-to-action marketing element, Hero marketing banner (landing page, Resume Reviewer marketing hero image asset, Illustrative product UI/dashboard concept, Purple/lilac hero color scheme

### Community 42 - "Common Schemas"
Cohesion: 0.50
Nodes (4): ErrorResponse, PaginatedResponse, BaseModel, Shared response schemas.

### Community 43 - "App Assets & React Logo"
Cohesion: 0.40
Nodes (5): Frontend Application (React SPA), React Brand Color #00D8FF, React Framework (UI Library), React Logo SVG Asset (Atom Symbol), Iconify Logos Icon Set

### Community 44 - "Favicon & Brand Mark"
Cohesion: 0.50
Nodes (5): Resume Reviewer Favicon, Lightning Bolt Logo Mark, SaaS Web App Brand Identity, Purple Gradient Brand Palette, Resume Reviewer SaaS Platform

### Community 45 - "Hero Visual Assets"
Cohesion: 0.60
Nodes (5): Hero Brand Illustration (hero.png), Brand Violet-Indigo Palette, Decorative Concentric Diamond / Gem Outline, Solid Inverted-Pyramid Gradient Core (funnel motif), Landing Hero Section (UploadSection area)

### Community 46 - "Logo & Scoring Mark"
Cohesion: 0.83
Nodes (4): DBN Brand Logo, DBN Wordmark Monogram, Monochrome Brand Identity, Resume Scoring Visual Metaphor

## Ambiguous Edges - Review These
- `Hero Brand Illustration (hero.png)` → `Landing Hero Section (UploadSection area)`  [AMBIGUOUS]
  frontend/src/assets/hero.png · relation: conceptually_related_to

## Knowledge Gaps
- **175 isolated node(s):** `verify-stack.sh script`, `dbn-resume-reviewer`, `$schema`, `typescript`, `oxc` (+170 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **37 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Hero Brand Illustration (hero.png)` and `Landing Hero Section (UploadSection area)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `Pytest` connect `Core Constants & Enums` to `Security & Test Setup`, `Score Parser & Validation`, `Scorer Timeout & Retry Logic`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Why does `Database` connect `DB Engine & Standard Routes` to `Core Constants & Enums`, `Analysis API Endpoints`, `DB Session Management`, `Analysis Service & Repository`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Why does `ResumeScorer` connect `Scorer Timeout & Retry Logic` to `Analysis API Endpoints`, `Score Parser & Validation`, `Analysis Service & Repository`, `LLM Provider Abstraction`, `Gemini/Claude Provider Classes`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `ScoreParseError` (e.g. with `ResumeScorer` and `._verify_overall()`) actually correct?**
  _`ScoreParseError` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `parse_score_response()` (e.g. with `weighted_overall()` and `Confidence`) actually correct?**
  _`parse_score_response()` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `ResumeScorer` (e.g. with `ScoreParseError` and `BaseLLMProvider`) actually correct?**
  _`ResumeScorer` has 11 INFERRED edges - model-reasoned connections that need verification._