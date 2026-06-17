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

---

## Phasing + recommendation

1. **C2 — incremental load** first. Biggest unlock (the HOT parked sources are big JSON APIs), the most
   contained change, **no browser dependency**. Prove it on **CFPB consumer complaints** (incremental by
   `date_received`) — the canonical case.
2. **C1a — static scrape** next (prompt/recon + bounded crawl).
3. **C1b — Playwright** last, only if a target source demands JS rendering.

**First concrete step:** implement `load_mode=incremental` in `ingest.py` + config/recon, and prove it
end to end on CFPB complaints.
