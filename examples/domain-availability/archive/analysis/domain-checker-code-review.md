# Domain Availability Checker - Code Review Report

**Review Date**: 2026-01-30
**Status**: CRITICAL RELIABILITY ISSUES IDENTIFIED

## Executive Summary

The optimization changes introduced **multiple critical reliability issues** that cause false positives. The root causes are:

1. **Race condition in concurrent execution** - unordered result processing
2. **Response parsing logic vulnerable to rate limiting** - AI extraction fails silently
3. **Missing error handling for partial responses**
4. **Concurrent access race conditions**
5. **No retry logic for rate-limited responses**

---

## Critical Issues

### 1. RACE CONDITION: Unordered Result Processing

**Location**: Lines 551-704

**Original Code** (correct):
```python
results: list[dict[str, Any]] = [None] * len(domains_to_check)  # Pre-allocated
# ... assigns to results[i] based on index
```

**Optimized Code** (incorrect):
```python
results: list[dict[str, Any]] = []  # APPENDED IN COMPLETION ORDER
results.append(result)  # LINE 654: WRONG ORDER
```

**Impact**: Domain-to-result mapping gets corrupted when results complete out of order.

### 2. Silent Rate Limiting Failure

**Location**: Lines 584-620

When InstantDomainSearch is rate-limited, it returns:
- Empty or null `extract` field
- Incomplete or cached `markdown` content
- Code interprets missing extract as "unknown" and defaults to markdown fallback
- Markdown fallback searches for "Continue" button without validating context

Test evidence: 155/196 domains (79%) showed `hasExtract: false` - indicating systematic extraction failures.

### 3. No Rate-Limit Detection

**Location**: Lines 370-422 in `firecrawl_scrape()`

```python
if isinstance(data, dict) and data.get("success") is False:
    raise RuntimeError(...)
return data  # Returns even if extract is null
```

Only raises if `success: false`. Doesn't check if response is complete/usable.

---

## Recommended Fixes (Priority Order)

### FIX 1: Revert to Pre-Allocated Array (CRITICAL - P0)

**Lines 551-704**:
```python
results: list[dict[str, Any] | None] = [None] * len(domains_to_check)

with ThreadPoolExecutor(max_workers=settings.concurrency) as pool:
    futures = {
        pool.submit(worker, domain, i + 1): i
        for i, domain in enumerate(domains_to_check)
    }
    for fut in as_completed(futures):
        i = futures[fut]
        results[i] = fut.result()  # Assign to correct index
```

### FIX 2: Add Rate-Limit Detection (CRITICAL - P0)

In `firecrawl_scrape()`:
```python
if isinstance(data, dict) and data.get("data"):
    data_obj = data.get("data")
    if data_obj.get("extract") is None:
        if len(data_obj.get("markdown", "")) < 200:
            raise RuntimeError("Rate limited: empty extract with minimal response")
```

### FIX 3: Reduce Concurrency (HIGH - P1)

**Lines 505-510**:
```python
concurrency=max(1, int(env("DOMAIN_CHECK_CONCURRENCY", "5") or "5")),  # Was 15
delay_ms=max(0, int(env("DOMAIN_CHECK_DELAY_MS", "200") or "200")),   # Was 100
```

Provides ~1.7x improvement over original while maintaining reliability.

---

## Summary Table

| Issue | Severity | Location | Fix |
|-------|----------|----------|-----|
| Unordered result processing | CRITICAL | Lines 551-704 | Pre-allocate array |
| Rate-limit silent failure | CRITICAL | Lines 370-422 | Validate extract completeness |
| Aggressive optimization | HIGH | Lines 505-510 | Reduce concurrency/delay |
| Markdown parsing logic | CRITICAL | Lines 310-313 | Change `if` to `elif` |

**Recommendation**: Implement all P0 + P1 fixes before rerunning the full domain check.
