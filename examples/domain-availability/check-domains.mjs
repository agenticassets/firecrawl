import { readFileSync, mkdirSync, writeFileSync, existsSync } from "node:fs";
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
  return raw
    .split(/\r?\n/)
    .map((l) => l.trim())
    .filter((l) => l && !l.startsWith("#"));
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

function inferAvailabilityFromMarkdown(markdown) {
  if (!markdown) return { availability: "unknown", price: null, notes: "No markdown" };

  const text = markdown.toLowerCase();
  let availability = "unknown";

  // Heuristics (best-effort)
  if (/(\bavailable\b|\bfor sale\b|\bregister\b)/i.test(markdown)) availability = "available";
  if (/(\btaken\b|\bregistered\b|\bunavailable\b)/i.test(markdown)) availability = "taken";

  const priceMatch = markdown.match(/\$[\d,]+(?:\.\d{2})?/);
  const price = priceMatch ? priceMatch[0] : null;

  return { availability, price, notes: "Parsed from markdown" };
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

async function main() {
  const repoRoot = resolve(process.cwd());
  const inputFile = resolve(repoRoot, "examples", "domain-availability", "domains.txt");
  const outDir = resolve(repoRoot, "examples", "domain-availability", "out");
  mkdirSync(outDir, { recursive: true });

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

  console.log(`Checking ${domains.length} domains via Firecrawl...`);
  console.log(`API: ${apiUrl}${scrapePath}`);

  const startedAt = new Date().toISOString();

  const results = await runPool(
    domains,
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

        if (availability === "unknown" && data.markdown) {
          const fallback = inferAvailabilityFromMarkdown(data.markdown);
          availability = fallback.availability;
          price = price ?? fallback.price;
          if (!notes) notes = fallback.notes;
        }

        if (perRequestDelayMs > 0) await sleep(perRequestDelayMs);

        console.log(`[${i + 1}/${domains.length}] ${domain}: ${availability}${price ? ` (${price})` : ""}`);

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
        console.log(`[${i + 1}/${domains.length}] ${domain}: ERROR (${message})`);

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
    startedAt,
    finishedAt,
    apiUrl,
    scrapePath,
    count: results.length,
    successCount: results.filter((r) => r.ok).length,
    failureCount: results.filter((r) => !r.ok).length,
    results,
  };

  const resultsJsonPath = resolve(outDir, "results.json");
  writeFileSync(resultsJsonPath, JSON.stringify(jsonOut, null, 2), "utf8");

  const csvHeader = [
    "domain",
    "availability",
    "price",
    "notes",
    "ok",
    "error",
    "searchUrl",
    "timestamp",
  ];

  const csvLines = [csvHeader.join(",")];
  for (const r of results) {
    csvLines.push(
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

  const resultsCsvPath = resolve(outDir, "results.csv");
  writeFileSync(resultsCsvPath, csvLines.join("\n"), "utf8");

  console.log("\nDone.");
  console.log(`- JSON: ${resultsJsonPath}`);
  console.log(`- CSV:  ${resultsCsvPath}`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
