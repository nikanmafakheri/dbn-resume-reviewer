# Project Principles

## Engineering Principles

1. **Async-first**: All I/O should be async. We use async SQLAlchemy, async HTTP clients, and async route handlers throughout.
2. **Separation of concerns**: Models → Repositories → Services → API. Each layer has a single responsibility.
3. **Testability**: Dependency injection throughout. Repositories and services can be mocked in tests.
4. **Fail gracefully**: Rate limiting falls back to in-memory when Redis is down. AI providers handle errors with descriptive messages.
5. **Security first**: Passwords hashed with bcrypt, JWTs with short expiry, SQL injection prevented by ORM.

## Product Principles

1. **Fast feedback**: Analysis should complete within 30 seconds. Users get immediate 202 responses with polling.
2. **Clear state**: Every operation has visible states (pending → processing → completed/failed).
3. **Mobile-first UI**: The frontend is responsive and works on all screen sizes.
4. **Configurable AI**: Users can choose their preferred AI provider (Gemini, OpenAI, Claude, OpenRouter).