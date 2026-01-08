#!/usr/bin/env python3
"""Research paper downloader (via Firecrawl).

Given a list of paper landing-page URLs (urls.txt), this script:
1) Scrapes each landing URL through Firecrawl (saves Markdown).
2) Discovers a PDF URL (via Firecrawl extract + HTML/Markdown heuristics + site fallbacks).
3) Downloads the PDF.

Outputs per run:
- out/runs/<runId>/results.json + results.csv
- out/runs/<runId>/<index>-<slug>/{page.md,metadata.json,paper.pdf}

Env vars:
- FIRECRAWL_API_KEY (required; or TEST_API_KEY)
- FIRECRAWL_API_URL (default: http://localhost:<PORT or 3002>)
- FIRECRAWL_SCRAPE_PATH (default: /v1/scrape)

Tuning:
- PAPER_DL_CONCURRENCY (default: 2)
- PAPER_DL_DELAY_MS (default: 250)
- PAPER_DL_WAITFOR_MS (default: 5000)
- PAPER_DL_TIMEOUT_MS (default: 90000)
- PAPER_DL_RETRIES (default: 2)
"""

from __future__ import annotations

import csv
import base64
import html as html_lib
import json
import os
import re
import time
import urllib.error
import urllib.parse
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

        if not (value.startswith('"') or value.startswith("'")):
            if "#" in value:
                value = value.split("#", 1)[0].strip()

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
    here = Path(__file__).resolve().parent
    dot = _find_dotenv(Path.cwd()) or _find_dotenv(here)
    if not dot:
        return None

    vals = _parse_dotenv(dot.read_text(encoding="utf-8"))
    for k, v in vals.items():
        if override or os.getenv(k) in (None, ""):
            os.environ[k] = v
    return dot


def safe_run_id_from_iso(iso: str) -> str:
    iso = re.sub(r"\.\d+Z$", "Z", iso)
    iso = re.sub(r"\+\d\d:\d\d$", "Z", iso)
    iso = iso.replace("-", "").replace(":", "").replace("T", "-")
    iso = re.sub(r"Z$", "", iso)
    return iso[:15]


def parse_urls_file(path: Path) -> list[str]:
    raw = path.read_text(encoding="utf-8")
    lines = []
    for line in raw.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        lines.append(s)

    seen: set[str] = set()
    out: list[str] = []
    for u in lines:
        k = u.strip()
        if not k:
            continue
        if k in seen:
            continue
        seen.add(k)
        out.append(k)
    return out


def slugify(value: str, max_len: int = 60) -> str:
    s = value.strip().lower()
    s = re.sub(r"https?://", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:max_len] if s else "item"


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
        "formats": ["extract", "markdown", "html"],
        "extract": {
            "prompt": (
                "You are extracting bibliographic info and the best PDF download link from a research paper landing page. "
                "Return ONLY a JSON object with keys: title (string or null), authors (array of strings), "
                "published (string or null), pdfUrl (string or null), and notes (string)."
            ),
            "schema": {
                "type": "object",
                "properties": {
                    "title": {"type": ["string", "null"]},
                    "authors": {"type": "array", "items": {"type": "string"}},
                    "published": {"type": ["string", "null"]},
                    "pdfUrl": {"type": ["string", "null"]},
                    "notes": {"type": "string"},
                },
                "required": ["title", "authors", "published", "pdfUrl", "notes"],
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
        with urllib.request.urlopen(req, timeout=max(10, settings.timeout_ms // 1000 + 10)) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            data = json.loads(raw)
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(raw)
            msg = parsed.get("error") or parsed.get("message") or f"HTTP {e.code}"
        except Exception:
            msg = f"HTTP {e.code}"
        raise RuntimeError(msg) from e

    if isinstance(data, dict) and data.get("success") is False:
        raise RuntimeError(data.get("error") or "Unknown Firecrawl error")

    return data


def firecrawl_scrape_pdf_base64(settings: Settings, pdf_url: str) -> dict[str, Any]:
    """Fetch a PDF through Firecrawl and return base64 bytes from data.markdown.

    Firecrawl returns PDF bytes encoded as base64 in the `markdown` field when `parsePDF: false`.
    """

    payload: dict[str, Any] = {
        "url": pdf_url,
        "formats": ["markdown"],
        "parsePDF": False,
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
        with urllib.request.urlopen(req, timeout=max(10, settings.timeout_ms // 1000 + 10)) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            data = json.loads(raw)
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(raw)
            msg = parsed.get("error") or parsed.get("message") or f"HTTP {e.code}"
        except Exception:
            msg = f"HTTP {e.code}"
        raise RuntimeError(msg) from e

    if isinstance(data, dict) and data.get("success") is False:
        raise RuntimeError(data.get("error") or "Unknown Firecrawl error")

    return data


def normalize_extract(extract: Any) -> dict[str, Any] | None:
    if extract is None:
        return None
    if isinstance(extract, dict):
        return extract
    if isinstance(extract, str):
        try:
            parsed = json.loads(extract)
            if isinstance(parsed, dict):
                return parsed
            return {"notes": extract}
        except Exception:
            return {"notes": extract}
    return None


def _absolute_url(base_url: str, maybe_url: str) -> str:
    return urllib.parse.urljoin(base_url, maybe_url)


def find_pdf_urls_in_text(text: str, base_url: str) -> list[str]:
    if not text:
        return []

    candidates: list[str] = []

    # 1) Any explicit http(s) .pdf
    for m in re.finditer(r"https?://[^\s\)\]\"']+\.pdf(?:\?[^\s\)\]\"']*)?", text, flags=re.I):
        candidates.append(html_lib.unescape(m.group(0)))

    # 2) Hrefs containing .pdf (relative)
    for m in re.finditer(r"href=\"([^\"]+\.pdf[^\"]*)\"", text, flags=re.I):
        candidates.append(_absolute_url(base_url, html_lib.unescape(m.group(1))))

    # 3) SSRN delivery links (often not ending in .pdf)
    for m in re.finditer(r"https?://[^\s\)\]\"']*(Delivery\.cfm\?[^\s\)\]\"']+)", text, flags=re.I):
        candidates.append(html_lib.unescape(m.group(0)))

    # 4) Wiley PDF endpoints may appear without .pdf extension
    for m in re.finditer(r"https?://[^\s\)\]\"']+/doi/(?:e?pdf|pdfdirect)/[^\s\)\]\"']+", text, flags=re.I):
        candidates.append(html_lib.unescape(m.group(0)))

    # De-dupe preserving order
    seen: set[str] = set()
    out: list[str] = []
    for u in candidates:
        u2 = u.strip()
        if not u2 or u2 in seen:
            continue
        seen.add(u2)
        out.append(u2)
    return out


def site_specific_pdf_fallbacks(landing_url: str) -> list[str]:
    """Generate likely PDF URLs if none discovered."""
    try:
        parsed = urllib.parse.urlparse(landing_url)
    except Exception:
        return []

    host = (parsed.netloc or "").lower()
    path = parsed.path or ""

    out: list[str] = []

    # Wiley: /doi/<doi> -> try /doi/epdf/<doi> and /doi/pdf/<doi>
    if host.endswith("onlinelibrary.wiley.com") and path.startswith("/doi/"):
        # keep existing query stripped
        base = f"{parsed.scheme}://{parsed.netloc}"
        doi = path[len("/doi/") :].lstrip("/")
        if doi:
            out.append(f"{base}/doi/epdf/{doi}")
            out.append(f"{base}/doi/pdf/{doi}")

    return out


def choose_best_pdf_url(urls: list[str]) -> str | None:
    if not urls:
        return None

    def score(u: str) -> tuple[int, int]:
        ul = u.lower()
        s = 0
        if ".pdf" in ul:
            s += 50
        if "epdf" in ul or "/pdf" in ul:
            s += 30
        if "download" in ul or "delivery.cfm" in ul:
            s += 20
        # Prefer shorter URLs if same score
        return (s, -len(u))

    return sorted(urls, key=score, reverse=True)[0]


def _looks_like_pdf_bytes(data: bytes) -> bool:
    if not data or len(data) < 200:
        return False
    head = data[:2048].lstrip()
    return b"%PDF-" in head[:1024]


def direct_download_pdf(url: str, *, timeout_s: int = 60) -> tuple[bytes, dict[str, Any]]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) FirecrawlExample/1.0",
            "Accept": "application/pdf,application/octet-stream;q=0.9,*/*;q=0.8",
        },
        method="GET",
    )

    with urllib.request.urlopen(req, timeout=timeout_s) as resp:
        content_type = (resp.headers.get("Content-Type") or "").split(";")[0].strip().lower()
        final_url = resp.geturl()
        data = resp.read()

    # Require real PDF bytes.
    if not _looks_like_pdf_bytes(data):
        raise RuntimeError(f"Non-PDF response (content-type={content_type}, finalUrl={final_url})")

    return data, {
        "method": "direct",
        "finalUrl": final_url,
        "contentType": content_type,
        "bytes": len(data),
    }


def firecrawl_download_pdf(settings: Settings, pdf_url: str) -> tuple[bytes, dict[str, Any]]:
    resp = firecrawl_scrape_pdf_base64(settings, pdf_url)
    data = (resp or {}).get("data") or {}
    b64 = data.get("markdown")
    if not isinstance(b64, str) or not b64.strip():
        raise RuntimeError("Firecrawl PDF fetch returned empty markdown")

    try:
        decoded = base64.b64decode(b64, validate=False)
    except Exception as e:
        raise RuntimeError("Failed to base64-decode Firecrawl PDF") from e

    if not _looks_like_pdf_bytes(decoded):
        raise RuntimeError("Firecrawl PDF fetch did not produce valid PDF bytes")

    return decoded, {
        "method": "firecrawl",
        "bytes": len(decoded),
    }


def download_pdf_best_effort(settings: Settings, pdf_url: str, out_path: Path) -> dict[str, Any]:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # 1) Try direct download (fast)
    try:
        data, meta = direct_download_pdf(pdf_url, timeout_s=max(20, settings.timeout_ms // 1000))
        out_path.write_bytes(data)
        return {"ok": True, **meta}
    except Exception as e:
        direct_err = str(e)

    # 2) Fallback to Firecrawl-powered PDF fetch
    data2, meta2 = with_retries(
        lambda: firecrawl_download_pdf(settings, pdf_url),
        retries=settings.retries,
        base_delay_s=0.5,
    )
    out_path.write_bytes(data2)
    return {"ok": True, **meta2, "directError": direct_err}


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
    load_dotenv(override=False)

    repo_root = Path.cwd()
    folder = repo_root / "examples" / "research-paper-downloader"
    input_file = folder / "urls.txt"
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
        concurrency=max(1, int(env("PAPER_DL_CONCURRENCY", "2") or "2")),
        delay_ms=max(0, int(env("PAPER_DL_DELAY_MS", "250") or "250")),
        waitfor_ms=max(0, int(env("PAPER_DL_WAITFOR_MS", "5000") or "5000")),
        timeout_ms=max(1000, int(env("PAPER_DL_TIMEOUT_MS", "90000") or "90000")),
        retries=max(0, int(env("PAPER_DL_RETRIES", "2") or "2")),
    )

    if not input_file.exists():
        print(f"Input file not found: {input_file}")
        return 1

    urls = parse_urls_file(input_file)
    if not urls:
        print(f"No URLs found in {input_file}")
        return 0

    started_at = utc_now_iso()
    run_id = safe_run_id_from_iso(started_at)
    run_out_dir = runs_dir / run_id
    run_out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Processing {len(urls)} URLs...")
    print(f"API: {settings.api_url}{settings.scrape_path}")

    def worker(url: str, index: int) -> dict[str, Any]:
        base: dict[str, Any] = {
            "index": index,
            "url": url,
            "timestamp": utc_now_iso(),
        }

        item_slug = slugify(url)
        item_dir = run_out_dir / f"{index:03d}-{item_slug}"
        item_dir.mkdir(parents=True, exist_ok=True)

        try:
            response = with_retries(
                lambda: firecrawl_scrape(settings, url),
                retries=settings.retries,
                base_delay_s=0.5,
            )

            data = (response or {}).get("data") or {}
            markdown = data.get("markdown") if isinstance(data, dict) else None
            html = data.get("html") if isinstance(data, dict) else None
            extracted = normalize_extract(data.get("extract"))

            page_md_path = item_dir / "page.md"
            page_md_path.write_text(markdown or "", encoding="utf-8")

            discovered: list[str] = []
            pdf_from_extract = (extracted or {}).get("pdfUrl")
            if isinstance(pdf_from_extract, str) and pdf_from_extract.strip():
                discovered.append(_absolute_url(url, html_lib.unescape(pdf_from_extract.strip())))

            # Heuristic scan in HTML/Markdown for PDF-ish URLs
            if isinstance(markdown, str) and markdown.strip():
                discovered.extend(find_pdf_urls_in_text(markdown, url))
            if isinstance(html, str) and html.strip():
                discovered.extend(find_pdf_urls_in_text(html, url))

            # Site fallbacks (e.g., Wiley epdf/pdf)
            discovered.extend(site_specific_pdf_fallbacks(url))

            # De-dupe preserving order
            seen: set[str] = set()
            pdf_candidates: list[str] = []
            for u in discovered:
                u2 = html_lib.unescape(u.strip())
                if not u2 or u2 in seen:
                    continue
                seen.add(u2)
                pdf_candidates.append(u2)

            pdf_result: dict[str, Any] | None = None
            pdf_error: str | None = None
            pdf_path: str | None = None
            chosen_pdf_url: str | None = None

            # Try candidates from best to worst until one yields a real PDF.
            candidates_sorted = sorted(
                pdf_candidates,
                key=lambda u: (1 if u == choose_best_pdf_url([u]) else 0),
                reverse=True,
            )
            # Ensure a stable, sensible ordering using the same scoring as choose_best_pdf_url
            # (by reusing the function across the full list)
            if pdf_candidates:
                best = choose_best_pdf_url(pdf_candidates)
                if best:
                    candidates_sorted = [best] + [u for u in pdf_candidates if u != best]

            for candidate in candidates_sorted:
                try:
                    if settings.delay_ms:
                        time.sleep(settings.delay_ms / 1000.0)

                    paper_pdf_path = item_dir / "paper.pdf"
                    pdf_result = download_pdf_best_effort(settings, candidate, paper_pdf_path)
                    pdf_path = str(paper_pdf_path)
                    chosen_pdf_url = candidate
                    pdf_error = None
                    break
                except Exception as e:
                    pdf_error = str(e)
                    continue

            meta = {
                "ok": True,
                "runId": run_id,
                "url": url,
                "title": (extracted or {}).get("title") if isinstance(extracted, dict) else None,
                "authors": (extracted or {}).get("authors") if isinstance(extracted, dict) else [],
                "published": (extracted or {}).get("published") if isinstance(extracted, dict) else None,
                "extractNotes": (extracted or {}).get("notes") if isinstance(extracted, dict) else "",
                "pdfCandidates": pdf_candidates,
                "pdfUrl": chosen_pdf_url,
                "pdfDownloaded": bool(pdf_result and pdf_result.get("ok")),
                "pdfDownload": pdf_result,
                "pdfError": pdf_error,
                "paths": {
                    "dir": str(item_dir),
                    "pageMarkdown": str(page_md_path),
                    "pdf": pdf_path,
                },
            }

            (item_dir / "metadata.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

            status = "pdf" if meta["pdfDownloaded"] else "no-pdf"
            print(f"[{index}/{len(urls)}] {status}: {url}")
            return {**base, **meta}

        except Exception as e:
            msg = str(e)
            print(f"[{index}/{len(urls)}] ERROR: {url} ({msg})")
            err = {**base, "ok": False, "runId": run_id, "error": msg}
            (item_dir / "metadata.json").write_text(json.dumps(err, indent=2), encoding="utf-8")
            return err

    results: list[dict[str, Any]] = [None] * len(urls)  # type: ignore[assignment]

    with ThreadPoolExecutor(max_workers=settings.concurrency) as pool:
        futures = {pool.submit(worker, url, i + 1): i for i, url in enumerate(urls)}
        for fut in as_completed(futures):
            i = futures[fut]
            results[i] = fut.result()

    finished_at = utc_now_iso()

    run_summary = {
        "runId": run_id,
        "startedAt": started_at,
        "finishedAt": finished_at,
        "apiUrl": settings.api_url,
        "scrapePath": settings.scrape_path,
        "count": len(results),
        "successCount": sum(1 for r in results if r.get("ok")),
        "pdfDownloadedCount": sum(1 for r in results if r.get("ok") and r.get("pdfDownloaded")),
        "failureCount": sum(1 for r in results if not r.get("ok")),
        "results": results,
    }

    (run_out_dir / "results.json").write_text(json.dumps(run_summary, indent=2), encoding="utf-8")

    csv_path = run_out_dir / "results.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "index",
                "ok",
                "url",
                "title",
                "published",
                "pdfUrl",
                "pdfDownloaded",
                "pdfError",
                "dir",
            ]
        )
        for r in results:
            w.writerow(
                [
                    r.get("index"),
                    bool(r.get("ok")),
                    r.get("url", ""),
                    r.get("title", "") if r.get("ok") else "",
                    r.get("published", "") if r.get("ok") else "",
                    r.get("pdfUrl", "") if r.get("ok") else "",
                    bool(r.get("pdfDownloaded")) if r.get("ok") else False,
                    r.get("pdfError", "") if r.get("ok") else r.get("error", ""),
                    (r.get("paths") or {}).get("dir", "") if r.get("ok") else "",
                ]
            )

    print("\nDone.")
    print(f"- Run JSON: {run_out_dir / 'results.json'}")
    print(f"- Run CSV:  {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
