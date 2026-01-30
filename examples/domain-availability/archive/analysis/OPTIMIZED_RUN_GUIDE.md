# Optimized Domain Checker - Quick Start Guide

## What's Optimized?

The `check-domains-optimized.py` script includes these performance improvements:

1. **Increased Concurrency**: 15 parallel threads (up from 3) = 5x faster
2. **Reduced Delay**: 100ms between requests (down from 250ms) = 2.5x faster
3. **Combined Speed-up**: ~12x faster overall (15/3 * 250/100 = 12.5x)
4. **Progress Tracking**: Real-time progress bar with tqdm
5. **Batch Checkpoints**: Auto-save every 20 domains for crash recovery
6. **Better Output**: Color-coded progress, summary stats, ETA

## Expected Performance

- **Original**: ~784 domains at 3 concurrency + 250ms delay = ~65 minutes
- **Optimized**: ~784 domains at 15 concurrency + 100ms delay = ~5 minutes

*Note: Actual time depends on API response times and your system resources.*

## Prerequisites

1. **Docker running** with Firecrawl services:
   ```powershell
   docker compose up -d
   docker ps  # Verify all 5 services are running
   ```

2. **Python 3.12+** installed

3. **Optional but recommended**: Install tqdm for progress bar:
   ```powershell
   pip install tqdm
   ```

## Quick Start

### Option 1: Use environment variables (PowerShell)

```powershell
# Set your API key
$env:FIRECRAWL_API_KEY = "your-api-key-here"

# Run the optimized script
python examples/domain-availability/check-domains-optimized.py
```

### Option 2: Create a .env file

```powershell
# Copy the example
cp examples/domain-availability/.env.optimized.example examples/domain-availability/.env

# Edit with your API key
notepad examples/domain-availability/.env

# Run
python examples/domain-availability/check-domains-optimized.py
```

## Tuning Parameters

If you want to go even faster (or slower for stability):

```powershell
# Ultra-fast mode (may stress your system)
$env:DOMAIN_CHECK_CONCURRENCY = 20
$env:DOMAIN_CHECK_DELAY_MS = 50

# Conservative mode (more stable, slower)
$env:DOMAIN_CHECK_CONCURRENCY = 10
$env:DOMAIN_CHECK_DELAY_MS = 200

# Run
python examples/domain-availability/check-domains-optimized.py
```

## Understanding the Output

### Progress Bar (with tqdm)
```
Checking domains: 45%|████████        | 354/784 [01:23<02:10, 3.3 domains/s] nexora.ai: available ($12.99)
```

### Without tqdm
```
[354/784] nexora.ai: available ($12.99)
```

### Summary Stats
```
============================================================
SUMMARY
============================================================
Total checked: 784
Success: 780
Failures: 4
Available domains: 156

Output files:
- Run JSON: examples/domain-availability/out/runs/20260130-143526/results.json
- Run CSV:  examples/domain-availability/out/runs/20260130-143526/results.csv
- Running JSON: examples/domain-availability/out/results.json
- Running CSV:  examples/domain-availability/out/results.csv
- Available: examples/domain-availability/out/available-domains.txt
============================================================
```

## Crash Recovery

The script saves checkpoints every 20 domains (configurable via `DOMAIN_CHECK_BATCH_SIZE`).

If the script crashes or you stop it:
- Already-checked domains are saved to `out/results.json`
- Simply re-run the script - it will skip already-checked domains
- No work is lost!

## Monitoring Docker Logs

To watch what's happening in real-time:

```powershell
# API logs
docker logs -f firecrawl-api-1 --tail 50

# Worker logs (if using separate workers)
docker logs -f firecrawl-worker-1 --tail 50
```

## Troubleshooting

### "Missing FIRECRAWL_API_KEY"
- Make sure you set the environment variable or created a .env file
- For .env: Must be in `examples/domain-availability/.env` OR repo root `.env`

### Script is slow / hanging
- Check Docker logs: `docker logs firecrawl-api-1 --tail 100`
- Verify services are healthy: `docker ps`
- Try reducing concurrency: `$env:DOMAIN_CHECK_CONCURRENCY = 5`

### High failure rate
- InstantDomainSearch may be rate-limiting
- Increase delay: `$env:DOMAIN_CHECK_DELAY_MS = 500`
- Reduce concurrency: `$env:DOMAIN_CHECK_CONCURRENCY = 5`

### Out of memory / system resources
- Your Docker setup may need more RAM
- Reduce concurrency: `$env:DOMAIN_CHECK_CONCURRENCY = 10`

## Comparison with Original Script

| Feature | Original | Optimized |
|---------|----------|-----------|
| Concurrency | 3 threads | 15 threads |
| Delay | 250ms | 100ms |
| Progress bar | No | Yes (with tqdm) |
| Batch checkpoints | No | Yes (every 20) |
| Summary stats | Basic | Detailed |
| Resume support | Yes | Yes |
| Est. time (784 domains) | ~65 min | ~5 min |

## Next Steps

After running the optimized script:

1. **Review available domains**: Check `out/available-domains.txt`
2. **Analyze results**: Open `out/results.csv` in Excel/Sheets
3. **Check pricing**: Review the price column for best deals
4. **Verify manually**: Visit InstantDomainSearch for final confirmation

## Advanced: Custom Settings Profile

Create custom profiles for different scenarios:

```powershell
# Profile: Speed (fast, may miss some)
$env:DOMAIN_CHECK_CONCURRENCY = 20
$env:DOMAIN_CHECK_DELAY_MS = 50
$env:DOMAIN_CHECK_WAITFOR_MS = 3000
$env:DOMAIN_CHECK_RETRIES = 1

# Profile: Accuracy (slower, very thorough)
$env:DOMAIN_CHECK_CONCURRENCY = 8
$env:DOMAIN_CHECK_DELAY_MS = 300
$env:DOMAIN_CHECK_WAITFOR_MS = 8000
$env:DOMAIN_CHECK_RETRIES = 3

# Profile: Balanced (recommended)
# Just use the defaults - no env vars needed!
```
