# Research paper downloader (via Firecrawl)

This example checks a list of paper landing-page URLs, **scrapes the page content** through the Firecrawl API (saved as Markdown), and then **downloads the associated PDF** when it can be discovered.

## What you edit
- `urls.txt`: one URL per line.

## What you run
From repo root:

```powershell
$env:FIRECRAWL_API_KEY = "fc-..."
# Optional:
$env:FIRECRAWL_API_URL = "http://localhost:3002"

python .\examples\research-paper-downloader\download-papers.py
```

## Output
Per run (timestamp-based run id):
- `out/runs/<runId>/results.json`
- `out/runs/<runId>/results.csv`
- `out/runs/<runId>/<index>-<slug>/page.md` (scraped page markdown)
- `out/runs/<runId>/<index>-<slug>/metadata.json` (extracted fields + pdf discovery)
- `out/runs/<runId>/<index>-<slug>/paper.pdf` (downloaded PDF, if found)

## Requirements
- Python 3.10+
- A Firecrawl API key in `FIRECRAWL_API_KEY` (or `TEST_API_KEY`)
- Optional: `FIRECRAWL_API_URL` (default: `http://localhost:<PORT or 3002>`)
- Optional: `FIRECRAWL_SCRAPE_PATH` (default: `/v1/scrape`)

The script will also try to auto-load the repo root `.env` if present (without overriding existing environment variables).

## Notes / caveats
- Some publishers block direct PDF downloads (403/paywalls). The script records the failure and keeps the scraped page markdown.
- SSRN and Wiley have site-specific fallbacks, but markup can change.
