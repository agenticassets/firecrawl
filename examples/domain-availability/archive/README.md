# Archive - Historical Analysis & Old Versions

This folder contains previous iterations, debugging analysis, and archived domain lists.

## Quick Navigation

### Analysis Documents (analysis/)

**Start here for bug investigation history**:
- `RESULTS_COMPARISON.md` - Before/after comparison showing false positive elimination
- `FIXES_APPLIED.md` - Summary of all 5 critical fixes
- `EVOLUTION_SUMMARY.md` - Executive summary of code evolution

**Deep dives**:
- `ARCHITECTURE_EVOLUTION.md` - How the code evolved from simple to concurrent
- `PARSING_EVOLUTION.md` - Code comparison across versions
- `GIT_COMMIT_TIMELINE.md` - Git history analysis
- `domain-checker-debug-analysis.md` - Root cause analysis of false positives
- `domain-checker-code-review.md` - Comprehensive code review findings

**Reference guides**:
- `ANALYSIS_INDEX.md` - Navigation guide to all analysis docs
- `QUICK_REFERENCE.md`, `EVOLUTION_QUICK_GUIDE.md` - Quick lookups
- `OPTIMIZATION_ANALYSIS.md`, `OPTIMIZED_RUN_GUIDE.md` - Performance tuning guides

### Old Scripts (scripts/)

- `check-domains.mjs` - Original Node.js version
- `check-domains.py` - Sequential Python version (pre-optimization, window-based parsing)

### Old Domain Lists (domain-lists/)

- `domains-test.txt` - Test domains used during debugging (dash.ai, ebit.ai, etc.)
- `domains-full.txt`, `domains-final-200.txt` - Previous full domain lists
- `new-ai-domains-to-check.txt` - Candidate domains
- `y-combinator-companies-2025-to-present.txt` - YC company domains
- `consolidated-ai-domains.md` - Research on AI domain landscape
- `latest-available-domains.txt` - Previous availability check results

## Key Findings Summary

**Root Cause**: Sequential `if` statements allowed "continue" keyword to overwrite "taken" status.

**Impact Timeline**:
- Original (Jan 8, commit 160d123b): Bug dormant (~0.5% manifestation)
- Window-based (Jan 8, commit e125f285): Bug critical (2.55% manifestation)
- Optimized aggressive (Jan 30): Bug + rate limiting = 5 false positives
- **Fixed optimized (Jan 30)**: 0 false positives, production-ready

**Performance**:
- Original: 23 min, very reliable
- Fixed optimized: 5 min, very reliable (4.6x faster)

See `analysis/RESULTS_COMPARISON.md` for complete details.
