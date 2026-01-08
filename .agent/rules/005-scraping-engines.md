---
trigger: always_on
---

# Scraping Engines & Workflow

Firecrawl uses various engines to handle different types of content and anti-bot challenges.

## Scrape Workflow

The entry point for scraping is `apps/api/src/scraper/scrapeURL/index.ts`.
- It selects the appropriate engine based on the URL and options.
- It manages retries, aborts, and timeouts.

## Engines

- **Playwright** (`src/scraper/scrapeURL/engines/playwright/`): Used for dynamic, JS-heavy websites.
- **Fire-engine** (`src/scraper/scrapeURL/engines/fire-engine/`): A more advanced engine for bypassing anti-bot measures (Cloud-only).
- **PDF/Media** (`src/scraper/scrapeURL/engines/pdf/`, etc.): Specialized parsers for non-HTML content.

## Adding or Modifying Engines

When working with engines:
1. **Interfaces**: Ensure the engine implements the expected interface for receiving metadata and returning results.
2. **Aborts & Timeouts**: Use `meta.abort.scrapeTimeout()` to respect the requested timeout.
3. **Error Reporting & Logging**: Map engine-specific errors to standard Firecrawl errors. Ensure all scrapes are logged to Supabase via the `logScrape` service.

## Resource Management

Scraping is resource-intensive.
- Ensure browsers (Playwright) are properly closed after use.
- Respect the `MAX_CPU` and `MAX_RAM` settings in the environment.

## Testing Engines

Engines should be tested with various scenarios:
- Normal HTML page.
- JS-rendered page.
- Blocked page (test retry logic).
- Large page/media.

Refer to `@apps/api/src/scraper/scrapeURL/index.ts` for the main orchestration logic.