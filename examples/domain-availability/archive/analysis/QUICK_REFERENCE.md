# Quick Reference - Optimized Domain Checker

## One-Liner Quick Start

```powershell
# Set API key and run (from repo root)
$env:FIRECRAWL_API_KEY = "your-api-key-here"; python examples/domain-availability/check-domains-optimized.py
```

---

## Essential Commands

### 1. Docker Management

```powershell
# Start Firecrawl services
docker compose up -d

# Check status (should see 5 services)
docker ps

# View API logs
docker logs -f firecrawl-api-1 --tail 50

# Stop services
docker compose down

# Restart services
docker compose restart
```

### 2. Run Domain Checker

```powershell
# With environment variable
$env:FIRECRAWL_API_KEY = "your-api-key"
python examples/domain-availability/check-domains-optimized.py

# With .env file (create once)
cp examples/domain-availability/.env.optimized.example examples/domain-availability/.env
notepad examples/domain-availability/.env
python examples/domain-availability/check-domains-optimized.py
```

### 3. Performance Tuning

```powershell
# Speed mode (faster)
$env:DOMAIN_CHECK_CONCURRENCY = 20
$env:DOMAIN_CHECK_DELAY_MS = 50

# Accuracy mode (slower, more reliable)
$env:DOMAIN_CHECK_CONCURRENCY = 8
$env:DOMAIN_CHECK_DELAY_MS = 300

# Check current settings (run will show them)
python examples/domain-availability/check-domains-optimized.py
```

### 4. Progress Monitoring

```powershell
# Install progress bar (optional, recommended)
pip install tqdm

# Watch output files in real-time (separate PowerShell window)
Get-Content examples/domain-availability/out/available-domains.txt -Wait
```

### 5. Results Analysis

```powershell
# View available domains
cat examples/domain-availability/out/available-domains.txt

# Open CSV in Excel
start examples/domain-availability/out/results.csv

# Count available domains
(cat examples/domain-availability/out/available-domains.txt).Count

# View latest run summary
cat examples/domain-availability/out/runs/*/results.json | tail -50
```

---

## Common Scenarios

### Scenario 1: First Run

```powershell
# 1. Start Docker
docker compose up -d

# 2. Verify services
docker ps

# 3. Set API key
$env:FIRECRAWL_API_KEY = "your-key"

# 4. Run checker
python examples/domain-availability/check-domains-optimized.py

# 5. Wait ~6 minutes for 784 domains
```

### Scenario 2: Resume After Crash

```powershell
# Just re-run - it will skip already-checked domains
python examples/domain-availability/check-domains-optimized.py
```

### Scenario 3: Check New Domains

```powershell
# 1. Add domains to domains.txt
notepad examples/domain-availability/domains.txt

# 2. Run - it will only check new domains
python examples/domain-availability/check-domains-optimized.py
```

### Scenario 4: Re-check All Domains

```powershell
# 1. Backup current results
cp examples/domain-availability/out/results.json examples/domain-availability/out/results.backup.json

# 2. Clear results
rm examples/domain-availability/out/results.json
rm examples/domain-availability/out/results.csv

# 3. Run fresh
python examples/domain-availability/check-domains-optimized.py
```

### Scenario 5: Troubleshooting High Failure Rate

```powershell
# 1. Check Docker logs
docker logs firecrawl-api-1 --tail 100

# 2. Reduce concurrency
$env:DOMAIN_CHECK_CONCURRENCY = 5

# 3. Increase delay
$env:DOMAIN_CHECK_DELAY_MS = 500

# 4. Re-run failed domains
python examples/domain-availability/check-domains-optimized.py
```

---

## Performance Presets

Copy-paste these for different scenarios:

### Preset: Conservative (High Accuracy)
```powershell
$env:DOMAIN_CHECK_CONCURRENCY = 5
$env:DOMAIN_CHECK_DELAY_MS = 300
$env:DOMAIN_CHECK_WAITFOR_MS = 8000
$env:DOMAIN_CHECK_RETRIES = 3
python examples/domain-availability/check-domains-optimized.py
```
**Time**: ~15 min | **Best for**: Final verification, premium domains

### Preset: Balanced (Recommended)
```powershell
# No need to set env vars - just run with defaults
python examples/domain-availability/check-domains-optimized.py
```
**Time**: ~6 min | **Best for**: General use, 784 domains

### Preset: Speed (Fast Screening)
```powershell
$env:DOMAIN_CHECK_CONCURRENCY = 20
$env:DOMAIN_CHECK_DELAY_MS = 50
$env:DOMAIN_CHECK_WAITFOR_MS = 3000
$env:DOMAIN_CHECK_RETRIES = 1
python examples/domain-availability/check-domains-optimized.py
```
**Time**: ~3 min | **Best for**: Initial screening, low-value domains

---

## Output Files Quick Reference

```
out/
├── results.json              # All runs combined (resume checkpoint)
├── results.csv               # All runs combined (Excel-friendly)
├── available-domains.txt     # Latest list of available domains
└── runs/
    └── 20260130-143526/      # Individual run (timestamped)
        ├── results.json      # This run only
        └── results.csv       # This run only
```

**What to check**:
- `available-domains.txt` - Your available domains list
- `results.csv` - Open in Excel, sort by price/availability
- Latest `runs/*/results.json` - Detailed run statistics

---

## Keyboard Shortcuts

| Action | Command |
|--------|---------|
| Stop script | `Ctrl+C` (graceful) |
| Force kill | `Ctrl+Break` |
| Pause output | `Ctrl+S` |
| Resume output | `Ctrl+Q` |
| Clear screen | `cls` |

---

## Environment Variables Cheat Sheet

```powershell
# Required
$env:FIRECRAWL_API_KEY = "sk-..."

# Performance (all optional)
$env:DOMAIN_CHECK_CONCURRENCY = 15      # Threads (default: 15)
$env:DOMAIN_CHECK_DELAY_MS = 100        # Delay ms (default: 100)
$env:DOMAIN_CHECK_WAITFOR_MS = 5000     # Page wait ms (default: 5000)
$env:DOMAIN_CHECK_TIMEOUT_MS = 60000    # Timeout ms (default: 60000)
$env:DOMAIN_CHECK_RETRIES = 2           # Retry count (default: 2)
$env:DOMAIN_CHECK_BATCH_SIZE = 20       # Checkpoint freq (default: 20)

# API settings (optional)
$env:FIRECRAWL_API_URL = "http://localhost:3002"
$env:FIRECRAWL_SCRAPE_PATH = "/v1/scrape"
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Missing FIRECRAWL_API_KEY" | Set `$env:FIRECRAWL_API_KEY = "your-key"` |
| No progress | Check `docker ps` - services must be running |
| High failure rate (>10%) | Reduce concurrency, increase delay |
| Script hangs | Check `docker logs firecrawl-api-1` |
| Out of memory | Reduce `DOMAIN_CHECK_CONCURRENCY` to 5-10 |
| Slow progress | Increase `DOMAIN_CHECK_CONCURRENCY` to 20-25 |
| No tqdm bar | Run `pip install tqdm` |

---

## Expected Output

### With tqdm (progress bar):
```
============================================================
OPTIMIZED DOMAIN CHECKER
============================================================
Total domains: 784
To check: 784
Skipped (already checked): 0
API: http://localhost:3002/v1/scrape
Concurrency: 15 threads
Delay: 100ms per request
Batch checkpoint: every 20 domains
============================================================

Checking domains: 45%|████████        | 354/784 [01:23<02:10, 3.3 domains/s] nexora.ai: available ($12.99)
```

### Without tqdm (plain text):
```
[354/784] nexora.ai: available ($12.99)
[355/784] orbix.ai: taken
[356/784] quantum.ai: ERROR (timeout)
```

### Final summary:
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

---

## Tips & Tricks

1. **Run in background**: Use `Start-Job` for async execution
   ```powershell
   $job = Start-Job { python examples/domain-availability/check-domains-optimized.py }
   Receive-Job $job -Wait
   ```

2. **Email results**: Combine with email script
   ```powershell
   python examples/domain-availability/check-domains-optimized.py
   # Then email available-domains.txt
   ```

3. **Schedule runs**: Use Task Scheduler for nightly checks

4. **Monitor multiple files**: Use `Get-Content -Wait` in separate windows

5. **Filter results**: Use PowerShell for quick analysis
   ```powershell
   # Domains under $20
   Import-Csv out/results.csv | Where { $_.price -match '\$([0-9]+)' -and [int]$Matches[1] -lt 20 }
   ```

---

## Getting Help

- **Script errors**: Check Docker logs: `docker logs firecrawl-api-1`
- **Docker issues**: Refer to `LOCAL_DEVELOPMENT_GUIDE.md`
- **Optimization details**: See `OPTIMIZATION_ANALYSIS.md`
- **Full guide**: See `OPTIMIZED_RUN_GUIDE.md`
