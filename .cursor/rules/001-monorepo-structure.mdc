---
description: Firecrawl monorepo structure, directory organization, and cross-app communication conventions.
globs: 
alwaysApply: true
---

# Monorepo Structure & Conventions

Firecrawl is organized as a monorepo with multiple applications and SDKs.

## Directory Layout

- `apps/api`: Main API server and background workers (Node.js/TypeScript).
- `apps/js-sdk`, `apps/python-sdk`, `apps/rust-sdk`: Official client libraries.
- `apps/test-suite`: Shared test infrastructure.
- `apps/ui/ingestion-ui`: React-based ingestion dashboard.
- `apps/nuq-postgres`: PostgreSQL/Supabase schema definitions and setup scripts.
- `apps/playwright-service-ts`: Microservice for browser-based scraping.
- `examples/`: Reference implementations and integration examples.

## Development Workflow

### API and Workers
The API and workers reside in `apps/api`. Use `pnpm harness` to start the environment for testing or local development.

### SDKs
When adding a feature to the API that should be exposed to users, ensure all official SDKs (`js-sdk`, `python-sdk`, `rust-sdk`) are updated to support the new functionality.

## Cross-App Communication

- The API communicates with background workers via BullMQ (Redis).
- SDKs communicate with the API via the REST endpoints defined in `apps/api/src/routes`.

## File Naming & Coding Style

- Use `kebab-case` for file and directory names.
- Prefer TypeScript for all new code.
- Follow existing patterns for versioning (e.g., `v1`, `v2` directories in controllers and routes).

## Adding New Dependencies

Before adding a new dependency:
1. Check if it's already used in another part of the monorepo.
2. Ensure it follows the project's licensing (AGPL-3.0 for core, MIT for SDKs).
3. Update the relevant `package.json` or equivalent dependency file.

## ⚠️ Shared Database Safety (CRITICAL)

The Supabase project used by Firecrawl is **shared with another AI application**. 
- **NEVER** modify, delete, or rename tables that use **CamelCase** (e.g., `Chat`, `User`, `Document`, `Message`, `VoiceSession`).
- **ONLY** interact with Firecrawl-specific tables (lowercase names like `requests`, `scrapes`, `crawls`, `api_keys`, `teams`).
- **EXERCISE EXTREME CAUTION** when running SQL migrations or RPC definitions to ensure zero impact on the existing application data.
