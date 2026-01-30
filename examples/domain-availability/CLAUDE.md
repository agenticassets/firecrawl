# Domain Availability Checker - Context for Claude

## What This Does

Bulk domain availability checker that scrapes InstantDomainSearch.com via Firecrawl API. Uses concurrent requests with AI extraction + markdown fallback parsing.

## Current State (2026-01-30)

**Production Script**: `check-domains-optimized.py`
- All critical bugs fixed (sequential if/elif, pre-allocated arrays, concurrency tuning)
- Performance: ~5 min for 200 domains
- Reliability: 0 false positives, >90% extraction success
- Settings: 8 workers, 150ms delay (balanced for reliability)

## Architecture

1. **Concurrent processing**: ThreadPoolExecutor with configurable workers/delays
2. **Dual extraction**:
   - Primary: AI-based extraction (fast, high accuracy when not rate-limited)
   - Fallback: Window-based markdown parsing (50-line window around domain)
3. **Results ordering**: Pre-allocated array indexed by domain position
4. **Checkpointing**: Incremental saves every batch for resumability

## Critical Code Patterns

### Markdown Parsing (Fixed)
```python
# Window-based parsing with proper elif chain
if "make offer" in window_text or "whois" in window_text:
    availability = "taken"
elif "continue" in window_text:  # MUST be elif, not if
    availability = "available"
```

**Why elif matters**: Sequential `if` allows "continue" to overwrite correct "taken" status when both keywords present (common in UI cards).

### Results Array (Fixed)
```python
# Pre-allocated to maintain domain order with concurrent completion
results = [None] * len(domains_to_check)
futures = {pool.submit(worker, domain, i): i for i, domain in enumerate(domains_to_check)}
for fut in as_completed(futures):
    i = futures[fut]
    results[i] = fut.result()  # Assign to correct index, not append
```

## Known Issues & Limitations

- InstantDomainSearch may change markup (requires maintenance)
- "Unknown" results require manual verification
- Not authoritative (use WHOIS/RDAP for production)
- Rate limiting possible if concurrency too high (>10 workers)

## Performance Trade-offs

| Setting | Speed | Reliability | Use Case |
|---------|-------|-------------|----------|
| 3 workers, 250ms | ~23 min | Very high | Conservative |
| 8 workers, 150ms | ~5 min | High | **Recommended** |
| 15 workers, 100ms | ~2 min | Low (rate limits) | Testing only |

## Archive Contents

- `archive/analysis/` - Complete debugging history, root cause analysis, architectural evolution
  - **Key docs**: `RESULTS_COMPARISON.md`, `FIXES_APPLIED.md`, `ARCHITECTURE_EVOLUTION.md`
- `archive/scripts/` - Old implementations (Node.js, sequential Python)
- `archive/domain-lists/` - Previous domain list iterations

## When Making Changes

1. **Test with small set** (`domains-test.txt` in archive if needed)
2. **Never change elif to if** in markdown parsing
3. **Maintain pre-allocated results array** pattern
4. **Don't increase concurrency beyond 10** without testing
5. **Update README.md** if config options change

## Dependencies

- Python 3.10+
- `requests` library
- Firecrawl API (local or cloud)
- Environment variables via `.env` file

## Testing

Run with test domains first:
```python
# Create test file with 5 domains
python check-domains-optimized.py -i test-domains.txt
# Verify no false positives before full run
```
