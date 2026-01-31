#!/usr/bin/env python3
"""Domain availability checker using Playwright + stealth.

Reads domains from a file (default: domains.txt), checks each on
InstantDomainSearch.com using a real browser with stealth to bypass
bot detection, and writes results to out/.

Usage:
    python check-domains-playwright.py                    # uses domains.txt
    python check-domains-playwright.py -i my-list.txt     # custom input
    python check-domains-playwright.py -i my-list.txt -w 3  # 3 workers

Environment variables (optional):
    DOMAIN_CHECK_CONCURRENCY  - parallel browser tabs (default: 4)
    DOMAIN_CHECK_DELAY_MS     - delay between checks in ms (default: 500)
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def safe_run_id(iso: str) -> str:
    iso = re.sub(r"\.\d+Z$", "Z", iso)
    iso = re.sub(r"\+\d\d:\d\d$", "Z", iso)
    iso = iso.replace("-", "").replace(":", "").replace("T", "-")
    return re.sub(r"Z$", "", iso)[:15]


def parse_domains(path: Path) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        k = s.lower()
        if k not in seen:
            seen.add(k)
            out.append(s)
    return out


def load_checked_domains(json_path: Path) -> set[str]:
    """Load already-checked domains from running results.json."""
    if not json_path.exists():
        return set()
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
        checked: set[str] = set()
        runs = data if isinstance(data, list) else [data] if isinstance(data, dict) else []
        for run in runs:
            for r in run.get("results", []):
                if isinstance(r, dict) and r.get("domain"):
                    checked.add(r["domain"].strip().lower())
        return checked
    except Exception:
        return set()


# ---------------------------------------------------------------------------
# Single-domain check using Playwright
# ---------------------------------------------------------------------------

def check_single_domain(domain: str, page) -> dict[str, Any]:
    """Check a single domain on InstantDomainSearch using an existing page."""
    url = f"https://instantdomainsearch.com/?q={domain}"
    result: dict[str, Any] = {
        "domain": domain,
        "searchUrl": url,
        "timestamp": utc_now_iso(),
    }

    try:
        page.goto(url, wait_until="networkidle", timeout=30000)
        time.sleep(3)  # Let dynamic content render

        text = page.inner_text("body")

        # Parse the text to find the domain and its status
        lines = text.split("\n")
        availability = "unknown"
        price = None
        notes_parts: list[str] = []

        # Look for the exact domain line and the line after it
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.lower() == domain.lower():
                # Check the next few lines for status indicators
                for j in range(i + 1, min(i + 8, len(lines))):
                    next_line = lines[j].strip().lower()
                    if next_line == "continue":
                        availability = "available"
                        notes_parts.append("'Continue' found after domain")
                        break
                    elif next_line in ("lookup", "make offer", "whois"):
                        availability = "taken"
                        notes_parts.append(f"'{lines[j].strip()}' found after domain")
                        break
                    elif next_line.startswith("$"):
                        availability = "taken"
                        price = next_line
                        notes_parts.append(f"Price {price} found")
                        break
                    elif next_line == "bookmark" or next_line == "copy url":
                        # These are action buttons for the main searched domain
                        continue
                    elif next_line == "pronounce" or next_line == "appraise" or next_line == "price history":
                        continue
                    elif next_line and not next_line.startswith("view the price"):
                        # If we hit something unexpected, keep looking
                        continue
                break

        # Also search in the extensions section for the specific TLD
        # Look for "domain.tld\nContinue" or "domain.tld\nLookup" pattern
        if availability == "unknown":
            for i, line in enumerate(lines):
                stripped = line.strip().lower()
                if stripped == domain.lower() and i + 1 < len(lines):
                    next_line = lines[i + 1].strip().lower()
                    if next_line == "continue":
                        availability = "available"
                        notes_parts.append("'Continue' in extensions section")
                    elif next_line in ("lookup", "make offer"):
                        availability = "taken"
                        notes_parts.append(f"'{lines[i+1].strip()}' in extensions section")
                    elif next_line.startswith("$"):
                        availability = "taken"
                        price = next_line
                        notes_parts.append(f"Price {price} in extensions")

        result["ok"] = True
        result["availability"] = availability
        result["price"] = price
        result["notes"] = "; ".join(notes_parts) if notes_parts else "Parsed from page text"

    except Exception as e:
        result["ok"] = False
        result["error"] = str(e)

    return result


# ---------------------------------------------------------------------------
# Batch processing (sequential - Playwright sync API requires single thread)
# ---------------------------------------------------------------------------

def check_domains_batch(
    domains: list[str],
    concurrency: int = 4,  # ignored for now; kept for API compat
    delay_ms: int = 500,
) -> list[dict[str, Any]]:
    """Check a batch of domains using Playwright with stealth (sequential)."""
    from playwright.sync_api import sync_playwright
    from playwright_stealth import Stealth

    results: list[dict[str, Any]] = []
    stealth = Stealth()

    print(f"\nChecking {len(domains)} domains sequentially...")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="en-US",
        )
        stealth.apply_stealth_sync(context)
        page = context.new_page()

        for i, domain in enumerate(domains):
            try:
                result = check_single_domain(domain, page)
            except Exception as e:
                result = {
                    "domain": domain,
                    "ok": False,
                    "error": str(e),
                    "timestamp": utc_now_iso(),
                }
            results.append(result)

            status = result.get("availability", "ERROR") if result.get("ok") else "ERROR"
            price_str = f" ({result.get('price')})" if result.get("price") else ""
            print(f"  [{i+1}/{len(domains)}] {domain}: {status}{price_str}")

            if delay_ms > 0 and i < len(domains) - 1:
                time.sleep(delay_ms / 1000.0)

        page.close()
        context.close()
        browser.close()

    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Check domain availability via Playwright")
    parser.add_argument("-i", "--input", default=None, help="Input file (default: domains.txt in script dir)")
    parser.add_argument("-w", "--workers", type=int, default=None, help="Concurrent workers (default: 4 or env)")
    parser.add_argument("--delay", type=int, default=None, help="Delay between checks in ms (default: 500)")
    parser.add_argument("--skip-checked", action="store_true", default=True, help="Skip already-checked domains")
    parser.add_argument("--no-skip", action="store_true", help="Check all domains even if already checked")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    input_file = Path(args.input) if args.input else script_dir / "domains.txt"
    out_dir = script_dir / "out"
    out_dir.mkdir(parents=True, exist_ok=True)
    runs_dir = out_dir / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)

    concurrency = args.workers or int(os.getenv("DOMAIN_CHECK_CONCURRENCY", "4"))
    delay_ms = args.delay if args.delay is not None else int(os.getenv("DOMAIN_CHECK_DELAY_MS", "500"))

    if not input_file.exists():
        print(f"Input file not found: {input_file}")
        return 1

    domains = parse_domains(input_file)
    if not domains:
        print(f"No domains in {input_file}")
        return 0

    # Skip already-checked
    running_json = out_dir / "results.json"
    skip_checked = not args.no_skip
    if skip_checked:
        checked = load_checked_domains(running_json)
        domains_to_check = [d for d in domains if d.lower() not in checked]
        skipped = len(domains) - len(domains_to_check)
    else:
        domains_to_check = domains
        skipped = 0

    print(f"\n{'='*60}")
    print("PLAYWRIGHT DOMAIN CHECKER")
    print(f"{'='*60}")
    print(f"Input: {input_file}")
    print(f"Total domains: {len(domains)}")
    print(f"To check: {len(domains_to_check)}")
    print(f"Skipped (already checked): {skipped}")
    print(f"Workers: {concurrency}")
    print(f"Delay: {delay_ms}ms")
    print(f"{'='*60}")

    if not domains_to_check:
        print("\nAll domains already checked!")
        return 0

    started_at = utc_now_iso()
    run_id = safe_run_id(started_at)

    results = check_domains_batch(domains_to_check, concurrency, delay_ms)

    finished_at = utc_now_iso()

    # Save run output
    run_out_dir = runs_dir / run_id
    run_out_dir.mkdir(parents=True, exist_ok=True)

    run_data = {
        "runId": run_id,
        "startedAt": started_at,
        "finishedAt": finished_at,
        "count": len(results),
        "successCount": sum(1 for r in results if r.get("ok")),
        "failureCount": sum(1 for r in results if not r.get("ok")),
        "skippedCount": skipped,
        "results": results,
    }

    (run_out_dir / "results.json").write_text(json.dumps(run_data, indent=2), encoding="utf-8")

    with (run_out_dir / "results.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["domain", "availability", "price", "notes", "ok", "error", "searchUrl", "timestamp"])
        for r in results:
            ok = bool(r.get("ok"))
            w.writerow([
                r.get("domain", ""),
                r.get("availability", "") if ok else "",
                r.get("price", "") if ok else "",
                r.get("notes", "") if ok else "",
                ok,
                "" if ok else r.get("error", ""),
                r.get("searchUrl", ""),
                r.get("timestamp", ""),
            ])

    # Update running results
    prior_runs = []
    if running_json.exists():
        try:
            data = json.loads(running_json.read_text(encoding="utf-8"))
            prior_runs = data if isinstance(data, list) else [data] if isinstance(data, dict) else []
        except Exception:
            pass

    all_runs = prior_runs + [run_data]
    running_json.write_text(json.dumps(all_runs, indent=2), encoding="utf-8")

    # Update available-domains.txt
    latest: dict[str, dict] = {}
    for run in all_runs:
        for r in run.get("results", []):
            if isinstance(r, dict) and r.get("domain"):
                latest[r["domain"].lower()] = r
    available = sorted(k for k, v in latest.items() if v.get("ok") and v.get("availability") == "available")
    (out_dir / "available-domains.txt").write_text("\n".join(available) + ("\n" if available else ""), encoding="utf-8")

    # Summary
    success = sum(1 for r in results if r.get("ok"))
    failures = sum(1 for r in results if not r.get("ok"))
    avail = sum(1 for r in results if r.get("ok") and r.get("availability") == "available")
    taken = sum(1 for r in results if r.get("ok") and r.get("availability") == "taken")
    unknown = sum(1 for r in results if r.get("ok") and r.get("availability") == "unknown")

    print(f"\n{'='*60}")
    print("RESULTS SUMMARY")
    print(f"{'='*60}")
    print(f"Total checked: {len(results)}")
    print(f"Success: {success} | Failures: {failures}")
    print(f"Available: {avail} | Taken: {taken} | Unknown: {unknown}")

    if avail > 0:
        print(f"\nAVAILABLE DOMAINS:")
        for r in results:
            if r.get("ok") and r.get("availability") == "available":
                price_str = f" ({r.get('price')})" if r.get("price") else ""
                print(f"  + {r['domain']}{price_str}")

    print(f"\nOutput: {run_out_dir}")
    print(f"{'='*60}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
