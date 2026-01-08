---
trigger: always_on
---

# AI & Data Extraction

Firecrawl provides advanced AI capabilities for scraping and structured data extraction.

## Core Extraction Logic

Extraction logic is primarily located in `apps/api/src/lib/extract/`.
- Support for both schema-based extraction (JSON schema) and prompt-based extraction.
- **Preferred Provider**: **OpenRouter** is the primary AI provider for this project.
- **Model Configuration**: Use `MODEL_NAME` in `.env` (e.g., `xiaomi/mimo-v2-flash:free`).
- **Logging**: All extraction jobs are logged to Supabase when DB authentication is enabled. 
    - Jobs via `/extract` are logged to the `extracts` table.
    - Jobs via `/scrape` with extraction formats are logged to the `scrapes` table.
- **⚠️ SAFETY**: When logging to Supabase, ensure you only interact with Firecrawl-specific tables. Do not affect any CamelCase tables belonging to the shared AI application.
- Support for multiple AI providers via the `ai` package and custom providers.

## Key Components

- **Extraction Service**: Orchestrates the extraction process across one or multiple URLs.
- **Generic AI Wrapper**: Located in `apps/api/src/lib/generic-ai.ts`, it provides a unified interface for different LLMs.

## Patterns

- **Schema Validation**: Use Zod or JSON Schema to define expected output structures.
- **Prompt Engineering**: System prompts for extraction are often defined in the service or in a shared prompts file.
- **Handling Multi-Page Extraction**: For wildcard URLs (e.g., `https://example.com/*`), ensure proper crawling before extraction.

## AI Gating in Tests

When writing tests for AI features, use the following gate:
```typescript
if (!process.env.TEST_SUITE_SELF_HOSTED || process.env.OPENAI_API_KEY || process.env.OLLAMA_BASE_URL) {
    // AI tests here
}
```

## Best Practices

- Prefer small, focused prompts for better extraction accuracy.
- Use `structured output` features of LLMs when available.
- Always handle token limits and truncate content if necessary using tiktoken or similar libraries.