# Domain Availability Checker

Fast, reliable bulk domain availability checker using Firecrawl API to scrape InstantDomainSearch.

## Quick Start

1. **Configure**:
   ```powershell
   cp .env.optimized.example .env
   # Edit .env and set FIRECRAWL_API_KEY
   ```

2. **Add domains** to `domains.txt` (one per line)

3. **Run**:
   ```powershell
   python check-domains-optimized.py
   ```

4. **Check results**:
   - `out/runs/<timestamp>/results.csv` - Latest run results
   - `out/available-domains.txt` - All available domains found

## Configuration

Edit `.env` or set environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `FIRECRAWL_API_KEY` | Required | Your Firecrawl API key |
| `FIRECRAWL_API_URL` | `http://localhost:3002` | API endpoint |
| `DOMAIN_CHECK_CONCURRENCY` | `8` | Parallel workers (8 recommended) |
| `DOMAIN_CHECK_DELAY_MS` | `150` | Delay between requests (150ms recommended) |

### Performance Tuning

- **Conservative** (slow, very reliable): `concurrency=3, delay_ms=250`
- **Balanced** (recommended): `concurrency=8, delay_ms=150` ← Default
- **Aggressive** (fast, may hit rate limits): `concurrency=15, delay_ms=100`

## Output Structure

```
out/
├── runs/
│   └── YYYYMMDD-HHMMSS/
│       ├── results.json    # Full structured data
│       └── results.csv     # Sortable/filterable
├── results.json            # Ledger of all runs
├── results.csv            # Combined CSV ledger
└── available-domains.txt  # Unique available domains
```

## Results Interpretation

- **available**: Domain can be registered
- **taken**: Domain is registered
- **unknown**: Could not determine (requires manual check)

Domains marked "unknown" should be verified manually at [InstantDomainSearch.com](https://instantdomainsearch.com).

## Requirements

- Python 3.10+
- Firecrawl API access (local or cloud)
- API key format: `fc-<uuid-without-dashes>` or raw UUID

## API Key Format

If using `USE_DB_AUTHENTICATION=true`:
- ✅ `fc-31dba252482749989356775a972cd48a` (no dashes)
- ✅ `31dba252-4827-4998-9356-775a972cd48a` (raw UUID)
- ❌ `fc-31dba252-4827-4998-9356-775a972cd48a` (fc- with dashes)

## Archived Files

- `archive/scripts/` - Old versions (Node.js, non-optimized Python)
- `archive/domain-lists/` - Previous domain list iterations
- `archive/analysis/` - Debugging analysis, bug fix documentation

## Notes

- Uses InstantDomainSearch UI scraping (not authoritative WHOIS)
- For production verification, use registrar/RDAP/WHOIS APIs
- False positives eliminated as of 2026-01-30 (see `archive/analysis/RESULTS_COMPARISON.md`)
