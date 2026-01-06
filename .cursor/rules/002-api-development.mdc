---
description: Patterns and conventions for API development in apps/api, including controllers, routes, and services.
globs: apps/api/src/**/*.ts
alwaysApply: true
---

# API Development (apps/api)

Guidelines for developing and maintaining the Firecrawl API.

## Architecture

The API follows a standard controller-route-service pattern:
- **Routes** (`src/routes/`): Define endpoints and apply middleware (auth, rate limiting).
- **Controllers** (`src/controllers/`): Handle request validation and response formatting. Versions (v0, v1, v2) are strictly separated.
- **Services** (`src/services/`): Contain business logic and interact with external systems (DB, Redis, Queues).
- **Lib** (`src/lib/`): Shared utilities, core logic, and third-party integrations.

## Versioning

Always maintain backward compatibility. New features should ideally be added to the latest version (`v2`) unless they are bug fixes for older versions.
- Path-based versioning: `/v1/scrape`, `/v2/scrape`.
- Directory-based code organization: `src/controllers/v1`, `src/controllers/v2`.

## Error Handling

Use the custom error classes defined in `@/apps/api/src/lib/error.ts`.
- `CustomError`: Base class for API errors.
- Ensure appropriate HTTP status codes are returned (400 for client errors, 401/403 for auth, 500 for server errors).

## Validation

- Use `Zod` for request body and query parameter validation.
- Define schemas in the controller or a shared types file.

## Performance & Resource Management

- **CPU/RAM Monitoring**: Workers should respect `MAX_CPU` and `MAX_RAM` thresholds.
- **Timeouts**: Always use `scrapeTimeout` for scraping operations to prevent hanging requests.

## Database Integration

- **PostgreSQL/Supabase**: Use Supabase for persistent data, authentication, and logging.
- **Enabling Auth**: Set `USE_DB_AUTHENTICATION=true` in `.env` to enable Supabase-backed authentication and persistent logging to `scrapes`, `crawls`, etc.
- **Initialization**: Use `apps/nuq-postgres/supabase-setup.sql` to initialize a new Supabase project with required tables and RPC mocks.
- **Persistent Storage**: Ensure the `scrapes` table has a `content` (TEXT) column and the `extracts` table has a `result` (JSONB) column to save scraped data and AI results.
- **Self-Hosted Mocks**: For self-hosted instances, use the mock RPCs (e.g., `auth_credit_usage_chunk_38`) provided in the setup script to bypass cloud credit logic.
- **Redis**: Used for caching, rate limiting, and task orchestration (BullMQ).

### ⚠️ Shared Database Caution
The connected Supabase instance is shared with a separate AI application.
- **DO NOT** touch tables starting with capital letters (e.g., `Chat`, `Message`).
- **DO NOT** perform destructive operations (`DROP`, `TRUNCATE`) on non-Firecrawl tables.
- All Firecrawl tables must remain **lowercase**.
