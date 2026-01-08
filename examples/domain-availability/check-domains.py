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
    return domains


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


def infer_from_markdown(markdown: str | None) -> dict[str, Any]:
    if not markdown:
        return {"availability": "unknown", "price": None, "notes": "No markdown"}

    text = markdown.lower()
    availability = "unknown"

    if "available" in text or "for sale" in text or "register" in text:
        availability = "available"
    if "taken" in text or "registered" in text or "unavailable" in text:
        availability = "taken"

    price = None
    # simple $123 or $1,234.56 scan
    import re

    m = re.search(r"\$[\d,]+(?:\.\d{2})?", markdown)
    if m:
        price = m.group(0)

    return {"availability": availability, "price": price, "notes": "Parsed from markdown"}


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

    print(f"Checking {len(domains)} domains via Firecrawl...")
    print(f"API: {settings.api_url}{settings.scrape_path}")

    started_at = utc_now_iso()

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

            if availability == "unknown" and data.get("markdown"):
                fallback = infer_from_markdown(data.get("markdown"))
                availability = fallback["availability"]
                if price is None:
                    price = fallback["price"]
                if not notes:
                    notes = fallback["notes"]

            if settings.delay_ms:
                time.sleep(settings.delay_ms / 1000.0)

            print(f"[{index}/{len(domains)}] {domain}: {availability}{f' ({price})' if price else ''}")

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
            print(f"[{index}/{len(domains)}] {domain}: ERROR ({msg})")
            return {**base, "ok": False, "error": msg}

    results: list[dict[str, Any]] = [None] * len(domains)  # type: ignore[assignment]

    with ThreadPoolExecutor(max_workers=settings.concurrency) as pool:
        futures = {
            pool.submit(worker, domain, i + 1): i
            for i, domain in enumerate(domains)
        }
        for fut in as_completed(futures):
            i = futures[fut]
            results[i] = fut.result()

    finished_at = utc_now_iso()

    out_json = {
        "startedAt": started_at,
        "finishedAt": finished_at,
        "apiUrl": settings.api_url,
        "scrapePath": settings.scrape_path,
        "count": len(results),
        "successCount": sum(1 for r in results if r.get("ok")),
        "failureCount": sum(1 for r in results if not r.get("ok")),
        "results": results,
    }

    json_path = out_dir / "results.json"
    json_path.write_text(json.dumps(out_json, indent=2), encoding="utf-8")

    csv_path = out_dir / "results.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
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

    print("\nDone.")
    print(f"- JSON: {json_path}")
    print(f"- CSV:  {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
