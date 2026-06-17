# Design — Incremental loads + Scrape extraction ("C")

Status: **proposed** (awaiting foreman approval) · 2026-06-17

## The gap

The agent today does exactly one kind of load: **snapshot-replace, bounded, all-TEXT mirror**
(`write_pandas overwrite=True`, idempotent by SHA-256). That breaks for two whole classes of catalog
source we keep hitting:

- **Huge / daily-growing** sources — CFPB complaints (millions, grows daily), ProPublica nonprofits,
  NPPES (~9 GB). You can't re-mirror millions of rows every run, and you want to **accumulate** new
  records, not replace the table.
- **Scrape** sources — per-hospital price files, JS-rendered portals, HTML listings. No extraction path
  (the agent fetches an API/CSV; a docs page now fails loudly via `_reject_html`, but that's a guard, not
  a capability).

Both batch-1 hard-fails (`fed_chronicling_america`, `fed_cms_hpt_mrf`) and the dequeued
`fed_cms_hpt_enforcement` land in these two buckets.

## Two orthogonal capabilities — do NOT conflate them

| | **What it changes** | **For** |
|---|---|---|
| **C2 — Incremental load** | how you *store* (accumulate vs replace) | huge / growing sources |
| **C1 — Scrape extraction** | how you *fetch* (HTML/JS, not API/CSV) | portal / per-entity sources |

They compose: a source can be `scrape + snapshot`, `api + incremental`, etc.

---

## C2 — Incremental load  (recommend FIRST)

### The idea
Landing becomes **append-only** for these sources. Each run fetches only records newer than a
**watermark**, appends them, and the existing staging dedup (`qualify row_number() … order by
_ingested_at desc`) resolves to current-state-per-key. This is the standard "insert-only raw + dedup in
transform" pattern.

### Mechanism (anchored to `ingest.run_ingest`)
1. Source config gains three fields (recon emits them): `load_mode: snapshot|incremental`,
   `cursor_field` (the watermark, e.g. `date_received`/`id`), `primary_key` (dedup key).
2. Incremental path:
   - `watermark = SELECT MAX(cursor_field) FROM landing` (NULL on first run → bounded initial backfill).
   - Pass `context["since"] = watermark` to `fetch_data`; the generated fetch pulls only `> watermark`
     (minus a small overlap margin to catch late arrivals).
   - **Append** (`write_pandas overwrite=False`, auto-create on first run), stamping the usual
     `_INGESTED_AT / _SOURCE_RUN_ID / _SRC_SHA256`.
   - Log the run (rows appended) to `INGEST_RUNS`.
3. Staging already dedups to latest-per-PK → clean current state for marts.

### Idempotency
Re-run with no new source data → fetch returns only the overlap window → appended → staging dedups it
away → **no net change** (a few duplicate PKs in landing, harmless). The SHA skip-if-unchanged doesn't
apply (incremental data always grows); idempotency comes from dedup-on-PK downstream.

### The trade-off  → this is the ADR
Incremental **breaks the raw-layer invariant** in `CLAUDE.md` ("snapshot-replace … running twice never
duplicates") for these sources: landing is now an append log, not a clean mirror.
- **Mitigation**: still all-TEXT, still fully provenance-stamped; the *clean* current state lives in
  staging (where consumers already read). Raw keeps every version (better lineage, not worse).
- **Verdict**: worth it — it's the only shape that fits growing sources, and it's a well-trodden pattern.

### Scope estimate
Contained: ~`ingest.py` (an incremental branch + watermark read), config/recon fields, codegen-prompt
guidance to honour `context["since"]`. No new dependencies.

---

## C1 — Scrape extraction  (phase 2–3)

- **C1a · static HTML (BeautifulSoup)** — *mostly already possible* (`beautifulsoup4` is installed,
  codegen can emit it, `access_pattern: scrape`, and `_reject_html` stops raw-HTML junk). Work =
  tighten recon + the codegen prompt for scrape, plus a **bounded per-entity crawl** helper (fetch
  index → follow ≤N links → parse each). Light.
- **C1b · JS-rendered (Playwright)** — new optional dependency + a headless-browser install + a
  `render(url)` helper. Heaviest (browser in the container). Only build when a real source needs it.
  **BUILT + PROVEN 2026-06-17** — see the C1b section below.

---

## C1b — Headless-browser scrape (Playwright)  ✅ BUILT + PROVEN

### The gap C1 Phase 1 left
Static scrape (requests + BeautifulSoup) only reaches data that's in the *initial* HTML. C1 Phase 1's
own finding: most accountability scrape targets are **JS-rendered** (the data is injected client-side,
so `requests` gets an empty shell) or **bot-protected** (a JS challenge — Cloudflare "Just a moment…",
"enable JavaScript" — served instead of content). Static BS4 can't pass either. BAILII (UK case law)
was the documented graceful-failure: the agent wrote correct BS4 code, then hit the bot wall.

### The capability
A new `render(url)` helper (`browser.py`) drives a real headless **Chromium via Playwright**: it loads
the page, runs its JavaScript, waits for the content to settle (or for a CSS selector), optionally
scrolls for lazy content, and returns the **fully-rendered HTML**. The generated `fetch_data()` parses
that HTML with BeautifulSoup / `pandas.read_html` **exactly like a static page** — the only thing that
changed is *how the bytes were fetched*.

### How the agent chooses it autonomously
Mirrors the C2 `load_mode` pattern — recon decides, the executor honours it:
1. **Recon** (`recon.txt`) gained a `scrape_js` value in the `access_pattern` enum, with guidance:
   use it *only* for a JS-rendered SPA or a bot wall; prefer file/API → `scrape` → `scrape_js`.
2. **Recon can now read walled pages.** `recon.fetch_page` detects a challenge / empty-shell response
   (`browser.looks_blocked`) and **escalates to the browser** to get the real page — so recon profiles
   the actual source, not the interstitial. Best-effort: falls back to the static shell if Playwright
   isn't installed.
3. **The LOAD executor** (`ingest._execute_fetch`) always injects `context["render"]`. The codegen prompt
   (`generate_ingest.txt`) tells Claude: for `scrape_js`, `html = context["render"](url)` (optionally
   `wait_selector=` / `scroll=True`), then parse with BS4. It never imports Playwright itself.

### The trade-offs  → this is the ADR
`scrape_js` is the heaviest path in the agent. We make it **opt-in per source**, not the default:

| Cost | Detail | Mitigation |
|---|---|---|
| **Heavy dependency** | Playwright ships a ~170 MB browser binary (`playwright install chromium`), separate from the pip package. | Optional dep: imported **lazily**, `render()` raises actionable install instructions, the rest of the agent runs without it. Only `scrape_js` sources pay. |
| **Slower** | A full browser launch + JS execution + network-settle is seconds per page vs milliseconds for `requests`. | Bounded crawl (≤25 sub-pages) still applies; recon prefers file/API/static scrape first. |
| **Heavier runtime** | Chromium needs real RAM/CPU and container libs (`playwright install-deps`); `--no-sandbox` + `--disable-dev-shm-usage` to run as root in a container. | Headless by default; one browser per `render()` call, closed in a `finally`. |
| **Fragile / arms-race** | Bot defences evolve; a real browser passes *basic* checks, not aggressive ones (hard CAPTCHAs, behavioural fingerprinting). | Fails loudly + lands no junk (the `_reject_html` shape guard still applies); the source stays queued for a retry. |
| **TLS behind a proxy** | Containers behind a TLS-intercepting proxy present a CA Chromium doesn't trust → `ERR_CERT_AUTHORITY_INVALID`. | `ignore_https_errors` default ON (`ONBOARD_BROWSER_IGNORE_HTTPS_ERRORS`); the raw layer still SHA-256s every payload. |

**Verdict:** worth it — it's the only path that reaches the bot-protected / JS-rendered accountability
sources (courts, portals), and the cost is fully contained to the sources that opt in.

### Proven live (2026-06-17) — same target, before vs after
`scripts/prove_c1b_bailii.py` runs **both** approaches through the real `ingest._execute_fetch`
(the exact LOAD-checkpoint path; only the Snowflake write is skipped). Target:
`https://www.bailii.org/uk/cases/UKSC/2024/`.

| Approach | Result |
|---|---|
| **BEFORE** — `scrape` (requests + BS4) | HTTP 200 but a **4.5 KB bot-challenge shell, 0 case links** → raises, **lands nothing** |
| **AFTER** — `scrape_js` (`context["render"]` + BS4) | challenge cleared, **44 UK Supreme Court 2024 judgments** (title + URL) into a clean DataFrame |

Recon autonomy independently verified: `recon.fetch_page` on the same URL detected the wall, rendered
through the browser, and returned the real case names (Potanina v Potanin, Paul v Royal Wolverhampton…).

---

## Phasing + recommendation

1. **C2 — incremental load** first. Biggest unlock (the HOT parked sources are big JSON APIs), the most
   contained change, **no browser dependency**. Prove it on **CFPB consumer complaints** (incremental by
   `date_received`) — the canonical case.
2. **C1a — static scrape** next (prompt/recon + bounded crawl).
3. **C1b — Playwright** last, only if a target source demands JS rendering.

**First concrete step:** implement `load_mode=incremental` in `ingest.py` + config/recon, and prove it
end to end on CFPB complaints.
