import { readFileSync, mkdirSync, writeFileSync, existsSync, appendFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

function parseDotEnvFile(dotEnvText) {
  const envs = {};
  for (const line of dotEnvText.split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;

    const eq = trimmed.indexOf("=");
    if (eq <= 0) continue;

    const key = trimmed.slice(0, eq).trim().replace(/^\uFEFF/, "");
    let value = trimmed.slice(eq + 1).trim();

    // Strip inline comments for unquoted values: KEY=value # comment
    if (!(value.startsWith('"') || value.startsWith("'"))) {
      const hash = value.indexOf("#");
      if (hash >= 0) value = value.slice(0, hash).trim();
    }

    // Strip surrounding quotes
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }

    if (key) envs[key] = value;
  }
  return envs;
}

function findDotEnvPath(startDir) {
  let cur = startDir;
  while (true) {
    const candidate = join(cur, ".env");
    if (existsSync(candidate)) return candidate;

    const parent = dirname(cur);
    if (parent === cur) return null;
    cur = parent;
  }
}

function loadDotEnv({ override = false } = {}) {
  const startDir = process.cwd();
  const dotEnvPath = findDotEnvPath(startDir) || findDotEnvPath(dirname(fileURLToPath(import.meta.url)));
  if (!dotEnvPath) return null;

  const envs = parseDotEnvFile(readFileSync(dotEnvPath, "utf8"));
  for (const [k, v] of Object.entries(envs)) {
    if (override || process.env[k] === undefined || process.env[k] === "") {
      process.env[k] = v;
    }
  }
  return dotEnvPath;
}

// Load repo .env if present (does not override existing env vars)
loadDotEnv();

function getEnv(name, fallback = undefined) {
  const val = process.env[name];
  return val === undefined || val === "" ? fallback : val;
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

function parseDomainsFile(filePath) {
  const raw = readFileSync(filePath, "utf8");
  const lines = raw
    .split(/\r?\n/)
    .map((l) => l.trim())
    .filter((l) => l && !l.startsWith("#"));

  // De-dupe while preserving order
  const seen = new Set();
  const out = [];
  for (const d of lines) {
    const k = d.toLowerCase();
    if (seen.has(k)) continue;
    seen.add(k);
    out.push(d);
  }
  return out;
}

function csvEscape(value) {
  if (value === null || value === undefined) return "";
  const str = String(value);
  if (/[",\n\r]/.test(str)) return `"${str.replace(/"/g, '""')}"`;
  return str;
}

function normalizeExtract(extract) {
  if (!extract) return null;
  if (typeof extract === "string") {
    try {
      return JSON.parse(extract);
    } catch {
      return { status: "unknown", notes: extract };
    }
  }
  if (typeof extract === "object") return extract;
  return null;
}

function inferAvailabilityFromMarkdown(markdown, domain) {
  if (!markdown) return { availability: "unknown", price: null, notes: "No markdown" };

  const lines = markdown.split(/\r?\n/);
  const domainNeedle = `[${domain}](`;
  const domainLineIndex = lines.findIndex((l) => l.includes(domainNeedle) || l.includes(domain));
  if (domainLineIndex < 0) {
    return { availability: "unknown", price: null, notes: "Domain not found in markdown" };
  }

  const windowStart = Math.max(0, domainLineIndex - 10);
  const windowEnd = Math.min(lines.length, domainLineIndex + 40);
  const windowLines = lines.slice(windowStart, windowEnd);
  const windowText = windowLines.join("\n").toLowerCase();

  // Availability: use local cues near the searched domain (avoid global marketing text).
  let availability = "unknown";
  if (windowText.includes("make offer") || windowText.includes("whois")) {
    availability = "taken";
  }
  if (windowText.includes("continue")) {
    availability = "available";
  }

  // Price: only accept a $ amount that appears to be associated with THIS domain.
  // The page often lists prices for other domains/extensions; we intentionally ignore those.
  let price = null;
  for (let i = domainLineIndex; i < Math.min(lines.length, domainLineIndex + 12); i++) {
    const line = lines[i].trim();

    // If we hit another domain link before a price, stop (price is likely for a different domain).
    if (i !== domainLineIndex && /^\[[^\]]+\]\([^)]*\)/.test(line) && line.includes(".") && !line.includes(domain)) {
      break;
    }

    // InstantDomainSearch prices often render as their own markdown link: [$12,345](...)
    const m = line.match(/\$[\d,]+(?:\.\d{2})?/);
    if (m) {
      price = m[0];
      break;
    }
  }

  const notesParts = [];
  if (availability === "available") notesParts.push("Found 'Continue' near domain");
  if (availability === "taken") notesParts.push("Found 'Make offer/WHOIS' near domain");
  if (price) notesParts.push("Found price near domain");
  if (!price) notesParts.push("No domain-specific price found");

  return {
    availability,
    price,
    notes: notesParts.join("; "),
  };
}

async function firecrawlScrape({ apiUrl, apiKey, scrapePath, url, timeoutMs, waitForMs }) {
  const body = {
    url,
    formats: ["extract", "markdown"],
    extract: {
      prompt:
        "You are checking domain availability on a domain search results page. Return ONLY a JSON object with keys: availability (one of available/taken/unknown), price (string or null), and notes (string).",
      schema: {
        type: "object",
        properties: {
          availability: {
            type: "string",
            enum: ["available", "taken", "unknown"],
          },
          price: { type: ["string", "null"] },
          notes: { type: "string" },
        },
        required: ["availability", "price", "notes"],
        additionalProperties: false,
      },
    },
    waitFor: waitForMs,
    timeout: timeoutMs,
  };

  const res = await fetch(`${apiUrl}${scrapePath}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  const json = await res.json().catch(() => null);
  if (!res.ok) {
    const msg = json?.error || json?.message || `HTTP ${res.status}`;
    const err = new Error(msg);
    err.status = res.status;
    err.response = json;
    throw err;
  }

  if (json?.success === false) {
    const msg = json?.error || "Unknown Firecrawl error";
    throw new Error(msg);
  }

  return json;
}

async function withRetries(fn, { retries, baseDelayMs }) {
  let lastErr;
  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      return await fn();
    } catch (err) {
      lastErr = err;
      if (attempt < retries) {
        await sleep(baseDelayMs * Math.pow(2, attempt));
      }
    }
  }
  throw lastErr;
}

async function runPool(items, worker, concurrency) {
  const results = new Array(items.length);
  let idx = 0;

  async function runner() {
    while (true) {
      const i = idx++;
      if (i >= items.length) return;
      results[i] = await worker(items[i], i);
    }
  }

  const workers = Array.from({ length: Math.max(1, concurrency) }, () => runner());
  await Promise.all(workers);
  return results;
}

function safeRunIdFromIso(iso) {
  // Windows-safe folder name
  // 2026-01-08T19:15:26.666Z -> 20260108-191526
  return iso
    .replace(/\.\d+Z$/, "Z")
    .replace(/\+\d\d:\d\d$/, "Z")
    .replace(/[-:]/g, "")
    .replace("T", "-")
    .replace(/Z$/, "")
    .slice(0, 15);
}

function loadRunningRunsJson(resultsJsonPath) {
  if (!existsSync(resultsJsonPath)) return [];
  try {
    const parsed = JSON.parse(readFileSync(resultsJsonPath, "utf8"));
    if (Array.isArray(parsed)) return parsed;
    if (parsed && typeof parsed === "object" && Array.isArray(parsed.results)) {
      // Old format: single run object
      return [parsed];
    }
    return [];
  } catch {
    return [];
  }
}

function buildCheckedDomainSetFromRuns(runs) {
  const checked = new Set();
  for (const run of runs) {
    const results = run?.results;
    if (!Array.isArray(results)) continue;
    for (const r of results) {
      const domain = r?.domain;
      if (typeof domain === "string" && domain.trim()) checked.add(domain.trim().toLowerCase());
    }
  }
  return checked;
}

function ensureRunningCsvHasV2Header(resultsCsvPath, headerV2) {
  if (!existsSync(resultsCsvPath)) return;
  const firstLine = readFileSync(resultsCsvPath, "utf8").split(/\r?\n/)[0] ?? "";
  if (firstLine.trim() === headerV2.join(",")) return;

  // Upgrade legacy v1 header to v2 by rewriting once.
  const legacyHeader = [
    "domain",
    "availability",
    "price",
    "notes",
    "ok",
    "error",
    "searchUrl",
    "timestamp",
  ].join(",");
  if (firstLine.trim() !== legacyHeader) return;

  const lines = readFileSync(resultsCsvPath, "utf8").split(/\r?\n/).filter(Boolean);
  const outLines = [headerV2.join(",")];
  for (let i = 1; i < lines.length; i++) {
    // Prefix empty run metadata for historical rows
    outLines.push(["", "", "", lines[i]].join(","));
  }
  writeFileSync(resultsCsvPath, outLines.join("\n") + "\n", "utf8");
}

function repairGluedCsvRows(resultsCsvPath) {
  if (!existsSync(resultsCsvPath)) return;
  const raw = readFileSync(resultsCsvPath, "utf8");
  if (!raw) return;

  const lines = raw.split(/\r?\n/);
  let changed = false;
  const out = [];

  // Detect a runId+timestamp sequence accidentally glued into the previous row.
  // Example: ...+00:0020260108-192516,2026-...
  const gluedMarker = /(\d{8}-\d{6},20\d{2}-\d{2}-\d{2}T)/;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (!line) {
      out.push(line);
      continue;
    }
    const match = gluedMarker.exec(line);
    if (match && match.index > 0) {
      changed = true;
      out.push(line.slice(0, match.index));
      out.push(line.slice(match.index));
    } else {
      out.push(line);
    }
  }

  if (!changed) return;

  let normalized = out.join("\n");
  if (!normalized.endsWith("\n")) normalized += "\n";
  writeFileSync(resultsCsvPath, normalized, "utf8");
}

function appendRowsToRunningCsv(resultsCsvPath, headerV2, rows) {
  if (!existsSync(resultsCsvPath)) {
    writeFileSync(resultsCsvPath, headerV2.join(",") + "\n", "utf8");
  }
  ensureRunningCsvHasV2Header(resultsCsvPath, headerV2);
  repairGluedCsvRows(resultsCsvPath);

  if (!rows.length) return;

  const existing = readFileSync(resultsCsvPath, "utf8");
  const firstLine = existing.split(/\r?\n/)[0] ?? "";
  if (firstLine.trim() !== headerV2.join(",")) {
    throw new Error(`Unexpected CSV header in ${resultsCsvPath}; refusing to append.`);
  }

  // Ensure the file ends with a newline before appending.
  if (existing.length > 0 && !existing.endsWith("\n")) {
    appendFileSync(resultsCsvPath, "\n", "utf8");
  }

  const data = rows.map((r) => r.map(csvEscape).join(",")).join("\n") + "\n";
  appendFileSync(resultsCsvPath, data, "utf8");
}

function writeAvailableDomainsTxt(outDir, runs) {
  // Derive a simple list from the running JSON ledger.
  // If a domain ever appears multiple times, the last occurrence wins.
  const latestByDomain = new Map();
  for (const run of runs) {
    const results = run?.results;
    if (!Array.isArray(results)) continue;
    for (const r of results) {
      const domain = typeof r?.domain === "string" ? r.domain.trim() : "";
      if (!domain) continue;
      const ok = !!r?.ok;
      const availability = typeof r?.availability === "string" ? r.availability : "";
      latestByDomain.set(domain.toLowerCase(), { domain, ok, availability });
    }
  }

  const available = [];
  for (const { domain, ok, availability } of latestByDomain.values()) {
    if (ok && availability === "available") available.push(domain.toLowerCase());
  }
  available.sort((a, b) => a.localeCompare(b));

  const txtPath = resolve(outDir, "available-domains.txt");
  writeFileSync(txtPath, available.join("\n") + (available.length ? "\n" : ""), "utf8");
  return txtPath;
}

async function main() {
  const repoRoot = resolve(process.cwd());
  const inputFile = resolve(repoRoot, "examples", "domain-availability", "domains.txt");
  const outDir = resolve(repoRoot, "examples", "domain-availability", "out");
  mkdirSync(outDir, { recursive: true });

  const runsDir = resolve(outDir, "runs");
  mkdirSync(runsDir, { recursive: true });

  const apiKey = getEnv("FIRECRAWL_API_KEY") ?? getEnv("TEST_API_KEY");
  if (!apiKey) {
    console.error("Missing FIRECRAWL_API_KEY (or TEST_API_KEY) environment variable");
    process.exit(1);
  }

  const defaultApiUrl = (() => {
    const port = getEnv("PORT", "3002");
    // HOST is often 0.0.0.0 for servers; use localhost for client calls.
    return `http://localhost:${port}`;
  })();

  const apiUrl = getEnv("FIRECRAWL_API_URL", defaultApiUrl).replace(/\/$/, "");
  const scrapePath = getEnv("FIRECRAWL_SCRAPE_PATH", "/v1/scrape");

  const concurrency = Number(getEnv("DOMAIN_CHECK_CONCURRENCY", "3"));
  const perRequestDelayMs = Number(getEnv("DOMAIN_CHECK_DELAY_MS", "250"));
  const waitForMs = Number(getEnv("DOMAIN_CHECK_WAITFOR_MS", "5000"));
  const timeoutMs = Number(getEnv("DOMAIN_CHECK_TIMEOUT_MS", "60000"));
  const retries = Number(getEnv("DOMAIN_CHECK_RETRIES", "2"));

  const domains = parseDomainsFile(inputFile);
  if (domains.length === 0) {
    console.log(`No domains found in ${inputFile}`);
    return;
  }

  const resultsJsonPath = resolve(outDir, "results.json");
  const resultsCsvPath = resolve(outDir, "results.csv");

  const priorRuns = loadRunningRunsJson(resultsJsonPath);
  const checkedDomains = buildCheckedDomainSetFromRuns(priorRuns);

  const domainsToCheck = domains.filter((d) => !checkedDomains.has(d.toLowerCase()));
  const skippedCount = domains.length - domainsToCheck.length;

  console.log(`Checking ${domainsToCheck.length} domains via Firecrawl...`);
  if (skippedCount > 0) {
    console.log(`Skipping ${skippedCount} already-checked domains (from out/results.json)`);
  }
  console.log(`API: ${apiUrl}${scrapePath}`);

  const startedAt = new Date().toISOString();
  const runId = safeRunIdFromIso(startedAt);
  const runOutDir = resolve(runsDir, runId);
  mkdirSync(runOutDir, { recursive: true });

  const results = await runPool(
    domainsToCheck,
    async (domain, i) => {
      const query = encodeURIComponent(domain);
      const searchUrl = `https://instantdomainsearch.com/?q=${query}`;

      const base = {
        domain,
        searchUrl,
        index: i + 1,
        timestamp: new Date().toISOString(),
      };

      try {
        const response = await withRetries(
          () =>
            firecrawlScrape({
              apiUrl,
              apiKey,
              scrapePath,
              url: searchUrl,
              timeoutMs,
              waitForMs,
            }),
          { retries, baseDelayMs: 500 }
        );

        const data = response?.data || {};
        const extracted = normalizeExtract(data.extract);

        let availability = extracted?.availability || extracted?.status || "unknown";
        if (!["available", "taken", "unknown"].includes(availability)) availability = "unknown";

        let price = extracted?.price ?? null;
        if (price !== null && typeof price !== "string") price = String(price);

        let notes = extracted?.notes ?? "";
        if (typeof notes !== "string") notes = JSON.stringify(notes);

        if (data.markdown) {
          const fallback = inferAvailabilityFromMarkdown(data.markdown, domain);

          if (availability === "unknown") {
            availability = fallback.availability;
          }

          if (price == null) {
            price = fallback.price;
          } else if (fallback.price == null) {
            // Avoid false positives where a $ amount is for a different domain on the page.
            price = null;
            notes = notes ? `${notes}; Dropped unverified price` : "Dropped unverified price";
          } else if (String(price) !== String(fallback.price)) {
            // Prefer domain-local price if it conflicts.
            price = fallback.price;
            notes = notes ? `${notes}; Replaced price with domain-local price` : "Replaced price with domain-local price";
          }

          if (!notes) notes = fallback.notes;
        }

        if (perRequestDelayMs > 0) await sleep(perRequestDelayMs);

        console.log(`[${i + 1}/${domainsToCheck.length}] ${domain}: ${availability}${price ? ` (${price})` : ""}`);

        return {
          ...base,
          ok: true,
          availability,
          price,
          notes,
          hasExtract: Boolean(data.extract),
          hasMarkdown: Boolean(data.markdown),
        };
      } catch (err) {
        if (perRequestDelayMs > 0) await sleep(perRequestDelayMs);

        const message = err?.message || String(err);
        console.log(`[${i + 1}/${domainsToCheck.length}] ${domain}: ERROR (${message})`);

        return {
          ...base,
          ok: false,
          error: message,
        };
      }
    },
    concurrency
  );

  const finishedAt = new Date().toISOString();

  const jsonOut = {
    runId,
    startedAt,
    finishedAt,
    apiUrl,
    scrapePath,
    count: results.length,
    successCount: results.filter((r) => r.ok).length,
    failureCount: results.filter((r) => !r.ok).length,
    skippedCount,
    results,
  };

  // Per-run outputs
  const runResultsJsonPath = resolve(runOutDir, "results.json");
  writeFileSync(runResultsJsonPath, JSON.stringify(jsonOut, null, 2), "utf8");


  const csvHeaderRun = [
    "domain",
    "availability",
    "price",
    "notes",
    "ok",
    "error",
    "searchUrl",
    "timestamp",
  ];

  const csvLinesRun = [csvHeaderRun.join(",")];
  for (const r of results) {
    csvLinesRun.push(
      [
        r.domain,
        r.ok ? r.availability : "",
        r.ok ? r.price ?? "" : "",
        r.ok ? r.notes ?? "" : "",
        r.ok,
        r.ok ? "" : r.error ?? "",
        r.searchUrl,
        r.timestamp,
      ]
        .map(csvEscape)
        .join(",")
    );
  }

  const runResultsCsvPath = resolve(runOutDir, "results.csv");
  writeFileSync(runResultsCsvPath, csvLinesRun.join("\n"), "utf8");

  // Append to running results
  const updatedRuns = [...priorRuns, jsonOut];
  writeFileSync(resultsJsonPath, JSON.stringify(updatedRuns, null, 2), "utf8");

  const csvHeaderV2 = [
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
  ];

  const csvRowsV2 = results.map((r) => [
    runId,
    startedAt,
    finishedAt,
    r.domain,
    r.ok ? r.availability : "",
    r.ok ? r.price ?? "" : "",
    r.ok ? r.notes ?? "" : "",
    r.ok,
    r.ok ? "" : r.error ?? "",
    r.searchUrl,
    r.timestamp,
  ]);

  appendRowsToRunningCsv(resultsCsvPath, csvHeaderV2, csvRowsV2);

  const availableTxtPath = writeAvailableDomainsTxt(outDir, updatedRuns);

  console.log("\nDone.");
  console.log(`- Run JSON: ${runResultsJsonPath}`);
  console.log(`- Run CSV:  ${runResultsCsvPath}`);
  console.log(`- Running JSON: ${resultsJsonPath}`);
  console.log(`- Running CSV:  ${resultsCsvPath}`);
  console.log(`- Available: ${availableTxtPath}`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
