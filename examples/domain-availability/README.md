# Domain availability checker (via Firecrawl)

This folder gives you a simple, repeatable workflow to check domain availability in bulk by scraping a domain search UI (InstantDomainSearch) through the Firecrawl API.

## What you edit
- `domains.txt`: one domain per line.

## What you run
- `check-domains.mjs`: Node version (reads `domains.txt`, scrapes `https://instantdomainsearch.com/?q=<domain>` through Firecrawl, extracts a structured status, and writes results).
- `check-domains.py`: Python version (same behavior as the Node script).

## Output
- Per-run outputs:
  - `out/runs/<runId>/results.json` (full structured results)
  - `out/runs/<runId>/results.csv` (easy to sort/filter)

- Running (append-only) outputs:
  - `out/results.json` (JSON array of run objects)
  - `out/results.csv` (CSV ledger of all rows across runs)

Re-running will skip domains already present in the running JSON ledger.

- Derived output:
  - `out/available-domains.txt` (unique, sorted list of domains whose latest known status is `available`)

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

### API key format (important)
If `USE_DB_AUTHENTICATION=true` is enabled on your Firecrawl API, the token must be either:
- The raw UUID with dashes (as stored in the `api_keys.key` column), e.g. `31dba252-4827-4998-9356-775a972cd48a`
- OR the `fc-` form **without dashes**, e.g. `fc-31dba252482749989356775a972cd48a`

If you use `fc-` *with* dashes (like `fc-31dba252-...`), the API will reject it as `Unauthorized: Invalid token`.

### Windows networking tip
If `http://localhost:3002` ever behaves oddly on Windows (e.g., an “Empty reply from server”), try:
- `http://127.0.0.1:3002`

## Notes / caveats
- This uses a third-party UI site (InstantDomainSearch). If they change markup or add bot protection, results can degrade.
- For “authoritative” availability, registrar/RDAP/WHOIS APIs are typically more reliable. This tool is meant for fast ideation and triage.

## Related
There is also a PowerShell version in `apps/api/scripts/check-domains.ps1`.
