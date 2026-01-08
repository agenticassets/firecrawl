#!/usr/bin/env python3
"""Bulk domain availability checker (via Firecrawl).

Reads domains from domains.txt, scrapes InstantDomainSearch via Firecrawl, and writes:
- out/results.json
- out/results.csv

Environment variables:
- FIRECRAWL_API_KEY (required)
- FIRECRAWL_API_URL (default: http://localhost:3002)
- FIRECRAWL_SCRAPE_PATH (default: /v1/scrape)

Tuning:
- DOMAIN_CHECK_CONCURRENCY (default: 3)
- DOMAIN_CHECK_DELAY_MS (default: 250)
- DOMAIN_CHECK_WAITFOR_MS (default: 5000)
- DOMAIN_CHECK_TIMEOUT_MS (default: 60000)
- DOMAIN_CHECK_RETRIES (default: 2)
"""

from __future__ import annotations

import csv
import json
import os
import re
import time
import urllib.parse
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def env(name: str, default: str | None = None) -> str | None:
    v = os.getenv(name)
    if v is None or v == "":
        return default
    return v


def _parse_dotenv(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if "=" not in s:
            continue
        key, value = s.split("=", 1)
        key = key.strip().lstrip("\ufeff")
        value = value.strip()

        # Strip inline comments for unquoted values: KEY=value # comment
        if not (value.startswith('"') or value.startswith("'")):
            if "#" in value:
                value = value.split("#", 1)[0].strip()

        # Strip surrounding quotes
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]

        if key:
            out[key] = value
    return out


def _find_dotenv(start: Path) -> Path | None:
    cur = start
    while True:
        candidate = cur / ".env"
        if candidate.exists():
            return candidate
        if cur.parent == cur:
            return None
        cur = cur.parent


def load_dotenv(*, override: bool = False) -> Path | None:
    """Load repo .env into os.environ (best-effort).

    - Does not override existing env vars by default.
    - Searches upward from CWD and from this script's directory.
    """

    here = Path(__file__).resolve().parent
    dot = _find_dotenv(Path.cwd()) or _find_dotenv(here)
    if not dot:
        return None

    vals = _parse_dotenv(dot.read_text(encoding="utf-8"))
    for k, v in vals.items():
        if override or os.getenv(k) in (None, ""):
            os.environ[k] = v
    return dot


def parse_domains_file(path: Path) -> list[str]:
    domains: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        domains.append(s)

    # De-dupe while preserving order
    seen: set[str] = set()
    out: list[str] = []
    for d in domains:
        k = d.lower()
        if k in seen:
            continue
        seen.add(k)
        out.append(d)
    return out


def safe_run_id_from_iso(iso: str) -> str:
    # Windows-safe folder name
    # 2026-01-08T19:15:26.666Z -> 20260108-191526
    iso = re.sub(r"\.\d+Z$", "Z", iso)
    iso = re.sub(r"\+\d\d:\d\d$", "Z", iso)
    iso = iso.replace("-", "").replace(":", "").replace("T", "-")
    iso = re.sub(r"Z$", "", iso)
    return iso[:15]


def load_running_runs_json(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(parsed, list):
            return [x for x in parsed if isinstance(x, dict)]
        if isinstance(parsed, dict) and isinstance(parsed.get("results"), list):
            # Old format: single run object
            return [parsed]
        return []
    except Exception:
        return []


def build_checked_domain_set_from_runs(runs: list[dict[str, Any]]) -> set[str]:
    checked: set[str] = set()
    for run in runs:
        results = run.get("results")
        if not isinstance(results, list):
            continue
        for r in results:
            if not isinstance(r, dict):
                continue
            domain = r.get("domain")
            if isinstance(domain, str) and domain.strip():
                checked.add(domain.strip().lower())
    return checked


def ensure_running_csv_has_v2_header(results_csv_path: Path, header_v2: list[str]) -> None:
    if not results_csv_path.exists():
        return

    try:
        first_line = results_csv_path.read_text(encoding="utf-8").splitlines()[0]
    except Exception:
        return

    if first_line.strip() == ",".join(header_v2):
        return

    legacy_header = ",".join(
        ["domain", "availability", "price", "notes", "ok", "error", "searchUrl", "timestamp"]
    )
    if first_line.strip() != legacy_header:
        return

    lines = [l for l in results_csv_path.read_text(encoding="utf-8").splitlines() if l]
    out_lines = [",".join(header_v2)]
    for line in lines[1:]:
        # Prefix empty run metadata for historical rows
        out_lines.append(",".join(["", "", "", line]))
    results_csv_path.write_text("\n".join(out_lines) + "\n", encoding="utf-8")


def append_rows_to_running_csv(results_csv_path: Path, header_v2: list[str], rows: list[list[Any]]) -> None:
    if not results_csv_path.exists():
        results_csv_path.write_text(",".join(header_v2) + "\n", encoding="utf-8")

    ensure_running_csv_has_v2_header(results_csv_path, header_v2)

    # Repair any previously glued rows caused by missing trailing newline.
    repair_running_csv_glued_rows(results_csv_path)

    first_line = results_csv_path.read_text(encoding="utf-8").splitlines()[0]
    if first_line.strip() != ",".join(header_v2):
        raise RuntimeError(f"Unexpected CSV header in {results_csv_path}; refusing to append.")

    if not rows:
        return

    with results_csv_path.open("a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        for row in rows:
            w.writerow(row)


def repair_running_csv_glued_rows(results_csv_path: Path) -> None:
    if not results_csv_path.exists():
        return

    raw = results_csv_path.read_text(encoding="utf-8")
    if not raw:
        return

    lines = raw.splitlines()
    out: list[str] = []
    changed = False

    glued_marker = re.compile(r"(\d{8}-\d{6},20\d{2}-\d{2}-\d{2}T)")
    for line in lines:
        m = glued_marker.search(line)
        if m and m.start() > 0:
            changed = True
            out.append(line[: m.start()])
            out.append(line[m.start() :])
        else:
            out.append(line)

    if not changed:
        return

    text = "\n".join(out)
    if not text.endswith("\n"):
        text += "\n"
    results_csv_path.write_text(text, encoding="utf-8")


def normalize_extract(extract: Any) -> dict[str, Any] | None:
    if extract is None:
        return None
    if isinstance(extract, dict):
        return extract
    if isinstance(extract, str):
        try:
            parsed = json.loads(extract)
            return parsed if isinstance(parsed, dict) else {"availability": "unknown", "notes": extract}
        except Exception:
            return {"availability": "unknown", "notes": extract}
    return None


def infer_from_markdown(markdown: str | None, domain: str) -> dict[str, Any]:
    if not markdown:
        return {"availability": "unknown", "price": None, "notes": "No markdown"}

    lines = markdown.splitlines()
    domain_needle = f"[{domain}]("
    domain_line_index = next((i for i, l in enumerate(lines) if domain_needle in l or domain in l), -1)
    if domain_line_index < 0:
        return {"availability": "unknown", "price": None, "notes": "Domain not found in markdown"}

    window_start = max(0, domain_line_index - 10)
    window_end = min(len(lines), domain_line_index + 40)
    window_lines = lines[window_start:window_end]
    window_text = "\n".join(window_lines).lower()

    availability = "unknown"
    if "make offer" in window_text or "whois" in window_text:
        availability = "taken"
    if "continue" in window_text:
        availability = "available"

    import re

    price: str | None = None
    for i in range(domain_line_index, min(len(lines), domain_line_index + 12)):
        line = lines[i].strip()

        # If we hit another domain-like link before a price, stop.
        if i != domain_line_index and re.match(r"^\[[^\]]+\]\([^)]*\)", line) and "." in line and domain not in line:
            break

        m = re.search(r"\$[\d,]+(?:\.\d{2})?", line)
        if m:
            price = m.group(0)
            break

    notes_parts: list[str] = []
    if availability == "available":
        notes_parts.append("Found 'Continue' near domain")
    if availability == "taken":
        notes_parts.append("Found 'Make offer/WHOIS' near domain")
    notes_parts.append("Found price near domain" if price else "No domain-specific price found")

    return {"availability": availability, "price": price, "notes": "; ".join(notes_parts)}


@dataclass(frozen=True)
class Settings:
    api_key: str
    api_url: str
    scrape_path: str
    concurrency: int
    delay_ms: int
    waitfor_ms: int
    timeout_ms: int
    retries: int


def firecrawl_scrape(settings: Settings, url: str) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "url": url,
        "formats": ["extract", "markdown"],
        "extract": {
            "prompt": (
                "You are checking domain availability on a domain search results page. "
                "Return ONLY a JSON object with keys: availability (one of available/taken/unknown), "
                "price (string or null), and notes (string)."
            ),
            "schema": {
                "type": "object",
                "properties": {
                    "availability": {"type": "string", "enum": ["available", "taken", "unknown"]},
                    "price": {"type": ["string", "null"]},
                    "notes": {"type": "string"},
                },
                "required": ["availability", "price", "notes"],
                "additionalProperties": False,
            },
        },
        "waitFor": settings.waitfor_ms,
        "timeout": settings.timeout_ms,
    }

    endpoint = f"{settings.api_url}{settings.scrape_path}"
    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {settings.api_key}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=max(5, settings.timeout_ms // 1000 + 5)) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            data = json.loads(raw)
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            data = json.loads(raw)
            msg = data.get("error") or data.get("message") or f"HTTP {e.code}"
        except Exception:
            msg = f"HTTP {e.code}"
        raise RuntimeError(msg) from e

    if isinstance(data, dict) and data.get("success") is False:
        raise RuntimeError(data.get("error") or "Unknown Firecrawl error")

    return data


def with_retries(fn, *, retries: int, base_delay_s: float = 0.5):
    last_exc: Exception | None = None
    for attempt in range(retries + 1):
        try:
            return fn()
        except Exception as e:
            last_exc = e
            if attempt < retries:
                time.sleep(base_delay_s * (2**attempt))
    assert last_exc is not None
    raise last_exc


def main() -> int:
    # Load repo .env if present (does not override existing env vars)
    load_dotenv(override=False)

    repo_root = Path.cwd()
    folder = repo_root / "examples" / "domain-availability"
    input_file = folder / "domains.txt"
    out_dir = folder / "out"
    out_dir.mkdir(parents=True, exist_ok=True)

    runs_dir = out_dir / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)

    api_key = env("FIRECRAWL_API_KEY") or env("TEST_API_KEY")
    if not api_key:
        print("Missing FIRECRAWL_API_KEY (or TEST_API_KEY) environment variable")
        return 1

    default_api_url = f"http://localhost:{env('PORT', '3002')}"
    api_url = (env("FIRECRAWL_API_URL", default_api_url) or "").rstrip("/")
    scrape_path = env("FIRECRAWL_SCRAPE_PATH", "/v1/scrape") or "/v1/scrape"

    settings = Settings(
        api_key=api_key,
        api_url=api_url,
        scrape_path=scrape_path,
        concurrency=max(1, int(env("DOMAIN_CHECK_CONCURRENCY", "3") or "3")),
        delay_ms=max(0, int(env("DOMAIN_CHECK_DELAY_MS", "250") or "250")),
        waitfor_ms=max(0, int(env("DOMAIN_CHECK_WAITFOR_MS", "5000") or "5000")),
        timeout_ms=max(1000, int(env("DOMAIN_CHECK_TIMEOUT_MS", "60000") or "60000")),
        retries=max(0, int(env("DOMAIN_CHECK_RETRIES", "2") or "2")),
    )

    if not input_file.exists():
        print(f"Input file not found: {input_file}")
        return 1

    domains = parse_domains_file(input_file)
    if not domains:
        print(f"No domains found in {input_file}")
        return 0

    running_json_path = out_dir / "results.json"
    running_csv_path = out_dir / "results.csv"

    prior_runs = load_running_runs_json(running_json_path)
    checked_domains = build_checked_domain_set_from_runs(prior_runs)
    domains_to_check = [d for d in domains if d.lower() not in checked_domains]
    skipped_count = len(domains) - len(domains_to_check)

    print(f"Checking {len(domains_to_check)} domains via Firecrawl...")
    if skipped_count > 0:
        print(f"Skipping {skipped_count} already-checked domains (from out/results.json)")
    print(f"API: {settings.api_url}{settings.scrape_path}")

    started_at = utc_now_iso()
    run_id = safe_run_id_from_iso(started_at)
    run_out_dir = runs_dir / run_id
    run_out_dir.mkdir(parents=True, exist_ok=True)

    def worker(domain: str, index: int) -> dict[str, Any]:
        search_url = f"https://instantdomainsearch.com/?q={urllib.parse.quote(domain)}"
        base: dict[str, Any] = {
            "domain": domain,
            "searchUrl": search_url,
            "index": index,
            "timestamp": utc_now_iso(),
        }

        try:
            response = with_retries(
                lambda: firecrawl_scrape(settings, search_url),
                retries=settings.retries,
                base_delay_s=0.5,
            )

            data = (response or {}).get("data") or {}
            extracted = normalize_extract(data.get("extract"))

            availability = (extracted or {}).get("availability") or (extracted or {}).get("status") or "unknown"
            if availability not in ("available", "taken", "unknown"):
                availability = "unknown"

            price = (extracted or {}).get("price", None)
            if price is not None and not isinstance(price, str):
                price = str(price)

            notes = (extracted or {}).get("notes", "")
            if notes is None:
                notes = ""
            if not isinstance(notes, str):
                notes = json.dumps(notes)

            if data.get("markdown"):
                fallback = infer_from_markdown(data.get("markdown"), domain)

                if availability == "unknown":
                    availability = fallback["availability"]

                if price is None:
                    price = fallback["price"]
                elif fallback["price"] is None:
                    price = None
                    notes = f"{notes}; Dropped unverified price" if notes else "Dropped unverified price"
                elif str(price) != str(fallback["price"]):
                    price = fallback["price"]
                    notes = (
                        f"{notes}; Replaced price with domain-local price" if notes else "Replaced price with domain-local price"
                    )

                if not notes:
                    notes = fallback["notes"]

            if settings.delay_ms:
                time.sleep(settings.delay_ms / 1000.0)

            print(f"[{index}/{len(domains_to_check)}] {domain}: {availability}{f' ({price})' if price else ''}")

            return {
                **base,
                "ok": True,
                "availability": availability,
                "price": price,
                "notes": notes,
                "hasExtract": bool(data.get("extract")),
                "hasMarkdown": bool(data.get("markdown")),
            }
        except Exception as e:
            if settings.delay_ms:
                time.sleep(settings.delay_ms / 1000.0)
            msg = str(e)
            print(f"[{index}/{len(domains_to_check)}] {domain}: ERROR ({msg})")
            return {**base, "ok": False, "error": msg}

    results: list[dict[str, Any]] = [None] * len(domains_to_check)  # type: ignore[assignment]

    with ThreadPoolExecutor(max_workers=settings.concurrency) as pool:
        futures = {
            pool.submit(worker, domain, i + 1): i
            for i, domain in enumerate(domains_to_check)
        }
        for fut in as_completed(futures):
            i = futures[fut]
            results[i] = fut.result()

    finished_at = utc_now_iso()

    out_json = {
        "runId": run_id,
        "startedAt": started_at,
        "finishedAt": finished_at,
        "apiUrl": settings.api_url,
        "scrapePath": settings.scrape_path,
        "count": len(results),
        "successCount": sum(1 for r in results if r.get("ok")),
        "failureCount": sum(1 for r in results if not r.get("ok")),
        "skippedCount": skipped_count,
        "results": results,
    }

    run_json_path = run_out_dir / "results.json"
    run_json_path.write_text(json.dumps(out_json, indent=2), encoding="utf-8")

    run_csv_path = run_out_dir / "results.csv"
    with run_csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["domain", "availability", "price", "notes", "ok", "error", "searchUrl", "timestamp"])
        for r in results:
            ok = bool(r.get("ok"))
            w.writerow(
                [
                    r.get("domain", ""),
                    r.get("availability", "") if ok else "",
                    r.get("price", "") if ok else "",
                    r.get("notes", "") if ok else "",
                    ok,
                    "" if ok else r.get("error", ""),
                    r.get("searchUrl", ""),
                    r.get("timestamp", ""),
                ]
            )

    # Append to running outputs
    updated_runs = prior_runs + [out_json]
    running_json_path.write_text(json.dumps(updated_runs, indent=2), encoding="utf-8")

    csv_header_v2 = [
        "runId",
        "runStartedAt",
        "runFinishedAt",
        "domain",
        "availability",
        "price",
        "notes",
        "ok",
        "error",
        "searchUrl",
        "timestamp",
    ]

    csv_rows_v2: list[list[Any]] = []
    for r in results:
        ok = bool(r.get("ok"))
        csv_rows_v2.append(
            [
                run_id,
                started_at,
                finished_at,
                r.get("domain", ""),
                r.get("availability", "") if ok else "",
                r.get("price", "") if ok else "",
                r.get("notes", "") if ok else "",
                ok,
                "" if ok else r.get("error", ""),
                r.get("searchUrl", ""),
                r.get("timestamp", ""),
            ]
        )

    append_rows_to_running_csv(running_csv_path, csv_header_v2, csv_rows_v2)

    print("\nDone.")
    print(f"- Run JSON: {run_json_path}")
    print(f"- Run CSV:  {run_csv_path}")
    print(f"- Running JSON: {running_json_path}")
    print(f"- Running CSV:  {running_csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
