# Domain availability checker (via Firecrawl)

This folder gives you a simple, repeatable workflow to check domain availability in bulk by scraping a domain search UI (InstantDomainSearch) through the Firecrawl API.

## What you edit
- `domains.txt`: one domain per line.

## What you run
- `check-domains.mjs`: Node version (reads `domains.txt`, scrapes `https://instantdomainsearch.com/?q=<domain>` through Firecrawl, extracts a structured status, and writes results).
- `check-domains.py`: Python version (same behavior as the Node script).

## Output
- `out/results.json` (full structured results)
- `out/results.csv` (easy to sort/filter)

## Requirements
- Node.js 18+ (uses built-in `fetch`)
- Python 3.10+
- A Firecrawl API key in `FIRECRAWL_API_KEY`
- A Firecrawl API base URL in `FIRECRAWL_API_URL` (optional)
  - Local default: `http://localhost:3002`
  - Cloud example: `https://api.firecrawl.dev`

Both scripts will also try to auto-load the repo root `.env` if present (without overriding existing environment variables). If you store your key as `TEST_API_KEY`, that works too.

## Run
From repo root:

```powershell
$env:FIRECRAWL_API_KEY = "fc-..."
# Optional:
$env:FIRECRAWL_API_URL = "http://localhost:3002"

node .\examples\domain-availability\check-domains.mjs
```

Python:

```powershell
$env:FIRECRAWL_API_KEY = "fc-..."
# Optional:
$env:FIRECRAWL_API_URL = "http://localhost:3002"

python .\examples\domain-availability\check-domains.py
```

## Notes / caveats
- This uses a third-party UI site (InstantDomainSearch). If they change markup or add bot protection, results can degrade.
- For “authoritative” availability, registrar/RDAP/WHOIS APIs are typically more reliable. This tool is meant for fast ideation and triage.

## Related
There is also a PowerShell version in `apps/api/scripts/check-domains.ps1`.
