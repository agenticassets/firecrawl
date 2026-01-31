# Domain Availability Checker

Bulk `.ai` domain availability checker using Playwright with stealth mode to scrape [InstantDomainSearch.com](https://instantdomainsearch.com).

## Quick Start

```bash
# 1. Install dependencies
pip install playwright playwright-stealth
playwright install chromium

# 2. Add domains to check (one per line)
echo "capro.ai" > domains.txt
echo "eqin.ai" >> domains.txt

# 3. Run
python check-domains-playwright.py

# 4. Results
cat out/available-domains.txt
```

## Usage

```bash
# Default: reads domains.txt, skips already-checked
python check-domains-playwright.py

# Custom input file
python check-domains-playwright.py -i my-list.txt

# Custom delay between checks (milliseconds)
python check-domains-playwright.py --delay 1000

# Force re-check all (ignore prior results)
python check-domains-playwright.py --no-skip
```

## Input Format

`domains.txt` (or any text file):
```
# Comments start with #
capro.ai
eqin.ai
equor.ai
```

One domain per line. Blank lines and `#` comments are ignored. Duplicates are auto-removed.

## Output

```
out/
├── runs/
│   └── 20260130-200236/
│       ├── results.json    # Structured data for this run
│       └── results.csv     # Spreadsheet-friendly format
├── results.json            # Append-only ledger of ALL runs
└── available-domains.txt   # Plain list of all available domains found
```

### Result Fields

| Field | Values | Meaning |
|-------|--------|---------|
| `availability` | `available` | Domain can be registered |
| `availability` | `taken` | Domain is registered or listed for sale |
| `availability` | `unknown` | Could not determine (verify manually) |
| `price` | `$X,XXX` or `null` | Listed price if domain is for sale |

## How It Works

1. Launches headless Chromium with [`playwright-stealth`](https://pypi.org/project/playwright-stealth/) to bypass Vercel bot detection
2. For each domain, loads `https://instantdomainsearch.com/?q={domain}`
3. Waits 3 seconds for dynamic JavaScript rendering
4. Reads the full page text and finds the domain name
5. Checks the lines immediately after the domain name:
   - **"Continue"** → available
   - **"Lookup" / "Make offer" / "WHOIS"** → taken
   - **"$..."** → taken (with price)
6. Saves per-run results and updates the running ledger

## Performance

- ~5 seconds per domain (3s render wait + 0.5s delay + overhead)
- 100 domains ≈ 8 minutes
- Sequential processing only (Playwright sync API limitation)

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `playwright` | 1.40+ | Browser automation |
| `playwright-stealth` | 2.0+ | Bot detection bypass |
| Chromium | via playwright | Headless browser |

No Firecrawl, no API keys, no Docker required.

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| All results "unknown" | Page structure changed | Inspect page manually, update text parsing |
| `greenlet.error` | Threading attempted | Don't use ThreadPoolExecutor - Playwright sync requires sequential |
| "Failed to verify browser" | Stealth not applied | Ensure `playwright-stealth` installed, `Stealth().apply_stealth_sync(context)` called |
| Timeout errors | Slow connection | Increase `--delay` and the `timeout=30000` in `page.goto()` |

## Agent Workflow: End-to-End Domain Search

This section describes the complete process for a coding agent to generate, filter, and check domain names.

### Step 1: Generate Candidates

Use sub-agents (or scripted generation) to brainstorm domain names. Effective strategies:

**Latin/finance roots** (highest quality):
- Prefixes: `cap`, `equ`, `val`, `fid`, `cre`, `luc`, `ten`, `bon`, `pro`, `aur`
- Suffixes: `-or`, `-ir`, `-irr`, `-in`, `-is`, `-ex`, `-ox`, `-ax`, `-on`
- Combine: `cap` + `ir` = `capir`, `equ` + `or` = `equor`

**Finance acronyms**: IRR, EBIT, CLTV, NOI, NAV, LTV, DCF, FFO, CAP

**Quality filters**:
- 4-5 letters preferred (6 acceptable, 7+ only if meaning is strong)
- Must contain at least 1 vowel per 2-3 consonants
- Must be pronounceable (no `xqzr` clusters)
- Must not be a common English word with negative connotations

Example generation script pattern:
```python
prefixes = ["cap", "equ", "val", "fid", "cre", "lev", "luc", "ten"]
suffixes = ["or", "ir", "in", "is", "ex", "ox", "ax", "on", "irr"]
candidates = [f"{p}{s}.ai" for p in prefixes for s in suffixes]
```

### Step 2: Deduplicate Against Prior Checks

```python
import json
from pathlib import Path

# Load all previously checked domains
results_json = Path("out/results.json")
checked = set()
if results_json.exists():
    for run in json.loads(results_json.read_text()):
        for r in run.get("results", []):
            checked.add(r["domain"].lower())

# Filter new candidates
new_domains = [d for d in candidates if d.lower() not in checked]
```

The script's `--skip-checked` flag (on by default) also handles this automatically.

### Step 3: Write Input File and Run

```bash
# Write candidates to file
python -c "
domains = ['aequi.ai', 'levir.ai', 'amort.ai']
with open('batch-check.txt', 'w') as f:
    f.write('\n'.join(domains))
"

# Check availability
python check-domains-playwright.py -i batch-check.txt
```

### Step 4: Review Results

```bash
# Quick view of available domains
cat out/available-domains.txt

# Detailed results from latest run
cat out/runs/*/results.csv | head -20

# Programmatic access
python -c "
import json
data = json.loads(open('out/results.json').read())
latest = data[-1]
available = [r['domain'] for r in latest['results'] if r.get('availability') == 'available']
print(f'Available: {len(available)}')
for d in available:
    print(f'  {d}')
"
```

### Step 5: Rank Results

Score available domains by relevance to the target industry:

```python
def score_domain(name: str) -> int:
    """Score a domain for CRE/PE/finance relevance. Higher = better."""
    s = 0
    # Length bonus
    n = name.replace('.ai', '')
    if len(n) == 4: s += 5
    elif len(n) == 5: s += 4
    elif len(n) == 6: s += 2
    # Finance root bonus
    roots = {'cap': 8, 'equ': 8, 'val': 7, 'fid': 7, 'cre': 7,
             'lev': 6, 'luc': 5, 'ten': 4, 'bon': 4, 'irr': 5}
    for root, pts in roots.items():
        if root in n.lower():
            s += pts
    # Ending quality
    for end in ['or', 'ir', 'in', 'is', 'ex', 'ax']:
        if n.lower().endswith(end):
            s += 3
            break
    # Pronounceability
    vowels = sum(1 for c in n if c in 'aeiou')
    if 0.3 <= vowels / len(n) <= 0.55:
        s += 3
    return s
```

## Archived / Deprecated

- `check-domains-optimized.py` - Firecrawl-based checker. **Blocked** by Vercel security checkpoint as of 2026-01-30. Kept for reference.
- `archive/scripts/` - Old Node.js and sequential Python implementations
- `archive/domain-lists/` - Previous domain list iterations
- `archive/analysis/` - Debugging history and architectural evolution docs

## Notes

- Results are from InstantDomainSearch UI scraping, **not authoritative WHOIS**
- Always verify with a registrar before purchasing
- See `TOP-20-RANKED.md` for curated recommendations for CRE/PE/finance AI
