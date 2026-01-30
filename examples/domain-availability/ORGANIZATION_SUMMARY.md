# Folder Organization - 2026-01-30

## What Was Done

Cleaned up and organized the domain-availability folder for clarity and ease of use.

## Current Structure

```
domain-availability/
├── README.md                      # Main guide (updated, concise)
├── CLAUDE.md                      # Context for Claude Code sessions
├── check-domains-optimized.py     # Production script (use this!)
├── .env.optimized.example         # Configuration template
├── domains.txt                    # Your domain list (edit this)
├── out/                          # Results directory
│   ├── runs/YYYYMMDD-HHMMSS/    # Per-run results
│   ├── results.json              # Ledger of all runs
│   ├── results.csv               # Combined CSV
│   └── available-domains.txt     # Available domains found
├── examples/                     # Example markdown files
│   ├── available-equor.md
│   └── unavailable-orbis.md
├── old/                          # Pre-existing old folder
│   └── domains copy.txt
└── archive/                      # Archived files (NEW)
    ├── README.md                 # Archive navigation guide
    ├── analysis/                 # All debugging/analysis docs (17 files)
    ├── domain-lists/             # Old domain lists (8 files)
    └── scripts/                  # Old versions (Node.js, old Python)
```

## What to Use

1. **Daily use**: `check-domains-optimized.py` with `domains.txt`
2. **Configuration**: Copy `.env.optimized.example` to `.env` and edit
3. **Documentation**: Read `README.md` for quick start
4. **Results**: Check `out/runs/<latest>/results.csv`

## What's Archived

### Analysis (archive/analysis/)
17 documents covering the complete debugging journey:
- Bug investigation and root cause analysis
- Before/after comparisons
- Code evolution timeline
- Performance analysis
- Fix documentation

**Key docs**: `RESULTS_COMPARISON.md`, `FIXES_APPLIED.md`, `EVOLUTION_SUMMARY.md`

### Domain Lists (archive/domain-lists/)
8 previous domain list iterations including:
- Test domains used during debugging
- Full domain lists from previous runs
- YC company domains
- AI domain research

### Scripts (archive/scripts/)
- `check-domains.mjs` - Original Node.js version
- `check-domains.py` - Sequential Python version (pre-optimization)

## Quick Start

```powershell
# 1. Configure
cp .env.optimized.example .env
# Edit .env and set FIRECRAWL_API_KEY

# 2. Add domains to domains.txt (one per line)

# 3. Run
python check-domains-optimized.py

# 4. Check results
cat out/available-domains.txt
```

## Notes

- Nothing was deleted, only organized
- All analysis documents preserved in `archive/analysis/`
- Production script (`check-domains-optimized.py`) has all bugs fixed
- Archive has its own README for navigation
