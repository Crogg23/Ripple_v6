# Build State
Last updated: 2026-06-17

## CURRENT FOCUS
The agent now has **three fetch capabilities** and picks each autonomously at recon: **bulk/API**,
**static scrape** (C1, BS4), and **headless-browser scrape** (C1b, Playwright `render()` for
JS-rendered / bot-protected pages) — plus two **load modes** (snapshot + C2 incremental). C1b is the
newest: proven live on BAILII (static scrape blocked by the bot wall → browser renders 44 UK Supreme
Court judgments). PR #2/#3 merged to `main`; PR #4 (C1 + C2) merged; C1b is on `claude/laughing-knuth-fmjka8`.

## WHAT EXISTS
- `library-onboarding/` — the 5-checkpoint CLI agent: RECON → SCRIPT → LOAD → DBT → REGISTRY.
- LOAD lands raw to `LIBRARY_RAW.LANDING.<UPPER(SOURCE_ID)>` — all columns TEXT, stamped
  `_INGESTED_AT` / `_SOURCE_RUN_ID` / `_SRC_SHA256`. Two load modes: **snapshot** (default — replace,
  idempotent by SHA) and **incremental** (C2 — read `MAX(cursor_field)` watermark, fetch only newer rows
  via `context["since"]`, append; staging dedups on the primary key). The LOAD also rejects HTML-as-data.
- Logs every run to `LIBRARY_META.INGEST_LOGS.INGEST_RUNS`; upserts `LIBRARY_META.REGISTRY.SOURCE_REGISTRY`.
- **Unattended**: `ONBOARD_AUTO_APPROVE=1` + `ONBOARD_AUTO_REPAIR=N` (default 3, feeds errors back to
  Claude). `live_batch.py` is the hand-curated growing queue — skips anything already landed, safe to re-run.
- **Registry-driven queue (B)**: `registry_queue.py` selects candidates from `SOURCE_REGISTRY`
  (not `INCLUDE='Y'`, not already landed, has URL, conforming `SOURCE_ID`, auth filter) ordered by
  `PRIORITY_TIER`; `registry_batch.py` runs them through the full agent. **Safe by default** — previews
  the queue read-only unless `--run`. Pinning each candidate's registry `SOURCE_ID` makes onboarding
  *update that row* (`INCLUDE` blank→`Y`), so the catalog is both the queue and the completion ledger.
- A minimal dbt project at `library-onboarding/ripple_dbt/` (run with the in-repo `profiles.yml`,
  creds from env / PAT-as-password, builds into the `DBT_CROGERS` schema).

### Live sources onboarded by the agent
| SOURCE_ID | rows | how |
|---|---|---|
| `fed_usaspending_toptier_agencies` | 111 | `first_live_load.py` (deterministic) |
| `fed_sec_edgar_company_tickers` | 10,414 | full LLM agent |
| `fed_federal_register_documents` | 5,000 | full LLM agent (codegen auto-paginated) |
| `fed_fdic_failed_banks` | 4,115 | full LLM agent (after URL-hallucination prompt fix) |
| `fed_treasury_debt_to_penny` | 8,329 | full LLM agent (full daily debt history) |
| `fed_fda_drug_enforcement` | 5,000 | full LLM agent (bounded sample) |
| `fed_treasury_avg_interest_rates` | 4,961 | full LLM agent (batch 3, 2026-06-17 — full monthly history 2001→2026) |
| `xc_biorxiv_medrxiv` | 432 | **registry-driven queue** (2026-06-17 — first source onboarded straight from the catalog) |
| `fed_clinicaltrials` | 500 | registry queue, tier-1 batch (bounded API snapshot) |
| `fed_cms_hcris` | 6,103 | registry queue, tier-1 batch (117-col hospital cost report; rebuilt against real columns) |
| `fed_cfpb_complaints` | 500 | **incremental (C2)** — 2 runs (backfill + watermark-advance append) |

**11 clean sources, ~45,465 raw rows.** Registry **901** rows, **14** `INCLUDE=Y` (CFPB +1; the dequeue
below −1). The false-success `fed_cms_hpt_enforcement` was dequeued (registry un-flagged + junk table
dropped, 2026-06-17, with Chris's OK): it had landed an HTML page (one `DOCTYPE_HTML` column, 22 junk
rows), not data — caught when its mart wouldn't build.

### Registry-driven queue (B) — `xc_biorxiv_medrxiv` (2026-06-17), verified live
- `registry_batch.py --source-id xc_biorxiv_medrxiv --run` selected the row from the catalog and ran the
  full agent. End to end: RECON → LOAD (432 rows → `LIBRARY_RAW.LANDING.XC_BIORXIV_MEDRXIV`) → DBT-gen →
  REGISTRY. The candidate's row flipped `INCLUDE` blank→`Y` **in place** — registry stayed **901** rows
  (an UPDATE via the pinned `SOURCE_ID`, not a duplicate INSERT), `INCLUDE=Y` went 10→11.
- **Agent fix this exposed**: dbt-gen returned the models as JSON with multi-line SQL/YAML values; for a
  wide (~25-col) table that JSON blew past `max_tokens=4096` and truncated → `extract_json` "Unbalanced
  JSON" → checkpoint 4 aborted before REGISTRY. Fixed: dbt-gen `max_tokens` 4096→8192, and `extract_json`
  now matches the fence greedily + parses with `strict=False` (tolerates literal newlines + dbt `{{ }}`).
- dbt models for biorxiv are GENERATED (staging view + `science_research` mart + schema.yml; `dbt parse`
  clean, 14 models total) but not yet RUN.

### Registry batch 1 — `registry_batch.py --tier 1 --limit 5 --run` (2026-06-17)
First real unattended batch off the catalog. **3/5 complete**, verified live:

| Source | Result | Rows |
|---|---|---|
| `fed_clinicaltrials` | ✅ onboarded, `INCLUDE=Y` | 500 |
| `fed_cms_hcris` | ✅ onboarded, `INCLUDE=Y` | 6,103 |
| `fed_cms_hpt_enforcement` | ✅ onboarded (auto-repair recovered a CSV-parse error) | 22 |
| `fed_chronicling_america` | ❌ aborted (3 repairs) — JS-heavy API docs page recon couldn't crack | — |
| `fed_cms_hpt_mrf` | ❌ aborted (3 repairs) — per-hospital MRF scrape (GitHub index) | — |

- Registry stayed **901** rows (3 in-place UPDATEs, no duplicates); `INCLUDE=Y` 11→14. **The 2 failures
  left zero partial state** — no landing table, no `INGEST_RUNS` row, registry untouched — so they remain
  queued for a retry. Clean graceful-failure behaviour.
- Takeaway: 60% landed, but **`dbt build` then exposed quality gaps the batch's "success" counter missed**
  (see hardening below). The real tally: 2 clean (clinicaltrials, biorxiv), 1 good-data-but-broken-models
  (cms_hcris, since fixed), 1 garbage (cms_hpt_enforcement HTML). Both hard-fails are scrape/JS shapes — the
  case for **C** (a scrape + incremental/bulk path).

### dbt build + agent hardening (2026-06-17) — `dbt build` the 4 newly-onboarded sources
Building the marts (not just generating models) surfaced two systemic agent bugs and got fixed:
- **`fed_cms_hpt_enforcement` was a false success**: the generated fetch hit a docs/landing URL, so pandas
  parsed an HTML page into one bogus column (`DOCTYPE_HTML`, 22 junk rows). The mart wouldn't build → caught.
  **Fix**: `ingest._reject_html()` now fails the LOAD loudly when the payload is an HTML page / single
  `<…>`/`DOCTYPE` column. Dequeued 2026-06-17 (Chris's OK): registry un-flagged, junk landing table dropped.
  Re-onboarding it later needs `--include-landed` (the bad run still sits in `INGEST_RUNS` history).
- **`fed_cms_hcris` staging wouldn't compile**: dbt-gen built SQL from recon's *guessed* schema
  (`PROVIDER_NUMBER`) but the CSV landed `PROVIDER_CCN` + 116 other real columns. **Fix**:
  `scaffold_dbt._actual_landing_columns()` introspects the real landing columns and generates against those;
  dbt-gen `max_tokens` 8192→16384 for very wide tables. Regenerated → builds green (mart = 6,103 rows).
- **Built green now**: `health__fed_clinicaltrials` (500), `science_research__xc_biorxiv_medrxiv` (432),
  `health__fed_cms_hcris` (6,103) — all materialized into `LIBRARY_MARTS.DBT_CROGERS`.

### C2 — incremental load (2026-06-17), built + proven live
The agent now does two load modes. **Incremental** (for huge/daily-growing sources): `run_ingest` reads the
`MAX(cursor_field)` watermark from landing, hands it to the fetch as `context["since"]`, fetches only newer
rows, and **appends** (`overwrite=False`); landing is an append log, staging dedups on the primary key.
First run (empty table) → bounded backfill; a run with no new rows → clean no-op (not an error).
- Touchpoints: `ingest.run_ingest` (+ `_watermark`, `_execute_fetch(since, allow_empty)`,
  `_load_landing(overwrite)`), `recon` emits `load_mode`/`cursor_field`/`primary_key`, prompts updated. No new deps.
- **Proven on CFPB consumer complaints** (`fed_cfpb_complaints`) — the canonical "wrong shape for snapshot"
  parked source: run 1 backfilled 250; run 2 **read watermark `2026-05-15T23:59:55Z`** and appended 250 more
  forward → landing **500**, 2 `INGEST_RUNS` rows, registered `INCLUDE=Y`. Append + watermark-advance confirmed.
- Trade-off (ADR in `docs/design-incremental-and-scrape.md`): incremental breaks the snapshot-replace raw
  invariant for these sources — landing becomes append-only. Mitigated: still all-TEXT + provenance; clean
  current state lives in staging.

### C1 — static scrape (Phase 1, 2026-06-17), built + proven
For sources with no clean file/API. Changes: codegen prompt gained scrape + bounded-crawl + browser-UA
guidance; `lxml` added to requirements (so `pandas.read_html` works); and **the HTML-guard was corrected**
— it now judges the DataFrame's *shape* (a single HTML-ish column = junk) instead of the raw bytes. The
old raw-bytes check wrongly rejected ALL legitimate scrapes (a scraped page's raw bytes are HTML by
definition); the shape check still catches the `fed_cms_hpt_enforcement`-style single-column junk.
- **Proven**: deterministic scrape of the "largest US companies by revenue" table (Wikipedia) → **100
  clean rows** (RANK/NAME/INDUSTRY/REVENUE/EMPLOYEES/HQ) into `LIBRARY_RAW.LANDING` (unregistered demo table).
- The **full agent** also wrote correct BS4 scrape code for BAILII UKSC cases and **failed gracefully** on
  BAILII's bot-detection wall (3 repairs → clean abort, no junk landed). Codegen quality confirmed.
- **KEY FINDING**: most accountability scrape targets are **bot-protected (BAILII) or JS-rendered**, so
  static BS4 has limited reach. **C1b (Playwright + a real browser session) is the actual unlock** for
  these — now a higher priority than originally scoped (evidence-driven).

### C1b — headless-browser scrape (Playwright, 2026-06-17), built + PROVEN live
The third fetch capability (after static `scrape`). For JS-rendered / bot-protected sources static BS4
can't reach. New `browser.py` exposes `render(url, wait_selector=, scroll=, timeout_ms=)` — drives a real
headless Chromium, runs the page JS, clears the bot challenge, returns fully-rendered HTML that the
generated `fetch_data` parses with BS4 exactly like a static page.
- **Agent chooses it autonomously** (mirrors C2's `load_mode`): recon's `access_pattern` enum gained
  `scrape_js`; `ingest._execute_fetch` always injects `context["render"]`; the codegen prompt tells Claude
  to use it for `scrape_js`. **Recon can now read walled pages too** — `fetch_page` detects a challenge /
  empty shell (`browser.looks_blocked`) and escalates to the browser to profile the real source.
- **Optional + heavy**: Playwright pip pkg is small but drives a ~170 MB browser (`playwright install
  chromium`). Imported **lazily** — the agent runs fine without it; `render()` raises actionable install
  steps. Only `scrape_js` sources pay the cost. Trade-offs ADR in `docs/design-incremental-and-scrape.md`
  (slower, heavier RAM/CPU, container libs, `--no-sandbox`, `ignore_https_errors` for proxied TLS, basic
  bot checks only — not hard CAPTCHAs).
- **PROVEN — same target, before vs after** (`scripts/prove_c1b_bailii.py`, run through the real
  `ingest._execute_fetch`): BAILII UK Supreme Court 2024 index
  (`https://www.bailii.org/uk/cases/UKSC/2024/`).
  - BEFORE (`scrape`, requests+BS4): HTTP 200 but a **4.5 KB bot-challenge shell, 0 case links** → raised,
    **landed nothing** (clean graceful failure — exactly the documented C1 wall).
  - AFTER (`scrape_js`, `context["render"]`+BS4): challenge cleared → **44 UK Supreme Court 2024
    judgments** (title + URL) into a clean DataFrame. Recon autonomy independently verified (read real
    case names through the browser).
- **NOTE on this container**: the live proof exercised the full RECON→SCRIPT→LOAD-*fetch* path (render
  injection + generated `fetch_data` + HTML-junk guard). The Snowflake **write** + real-LLM codegen
  weren't run here (this session's `SNOWFLAKE_PAT`/`ANTHROPIC_API_KEY` are read-only/placeholder; the
  Snowflake MCP is `CLAUDE_MCP_READONLY`). That plumbing is unchanged from C1 and already proven — what
  C1b adds is the fetch capability, and that's what's proven live.

### Batch 3 — `fed_treasury_avg_interest_rates` (2026-06-17), verified live
- LOAD → `LIBRARY_RAW.LANDING.FED_TREASURY_AVG_INTEREST_RATES` = **4,961 rows**, run `4046bcc7…`,
  sha `7fe37899…` (the same sha is on every row's `_SRC_SHA256` and on the `INGEST_RUNS` row — provenance chain intact).
- `INGEST_RUNS` → one `success` row (4,961 rows, 1.65 MB, ~11s).
- `SOURCE_REGISTRY` → new `INCLUDE=Y` row (Economy / Federal Debt & Interest Rates; join keys
  `record_date, security_type_desc, security_desc`). The curated `fed_fiscaldata_treasury` family row was NOT clobbered.
- Verified independently with the read-only MCP role (`CLAUDE_MCP_READONLY`); the agent wrote via the
  env PAT (`ACCOUNTADMIN`).
- **dbt for batch 3 is RUN** (2026-06-17): `dbt build` created the staging view
  `stg_fed_treasury_avg_interest_rates__avg_interest_rates` (`LIBRARY_STAGING.DBT_CROGERS`) + the mart table
  `economics__fed_treasury_avg_interest_rates` (`LIBRARY_MARTS.DBT_CROGERS`, 4,961 rows, surrogate key 1:1
  unique). Final: **PASS=18, WARN=0, ERROR=0**. One fix: the agent's `accepted_values` on
  `security_type_desc` was wrong (guessed five `Total *` labels from a *different* Treasury dataset) —
  corrected to the 3 real categories `Marketable / Non-marketable / Interest-bearing Debt` (a real guard,
  not downgraded to warn, since the categories are stable + exhaustive across the full history).

- **dbt is RUN** (batches 1–3): all **12 models** (6 sources × staging view + mart table) build into
  `LIBRARY_STAGING.DBT_CROGERS` / `LIBRARY_MARTS.DBT_CROGERS` — 0 errors. (USAspending agencies has no dbt
  models — its first load skipped checkpoint 4.)

## DECISIONS MADE
- **Snowflake cleanup + rebrand (2026-06-17, Chris ran the DDL).** Dropped dead DBs (`RIPPLE` v3,
  `RIPPLE_PRESERVE` [empty — vault never populated], `STORMS`, `STORM_LOCATIONS`, `WEATHER_PROJECT`,
  `TEST`) + the two `DISASTER_IMPACT.PUBLIC.MY_*_DBT_MODEL` tutorial leftovers. **Renamed the live
  Library DBs**: `RIPPLE_RAW→LIBRARY_RAW`, `RIPPLE_META→LIBRARY_META`, `RIPPLE_STAGING→LIBRARY_STAGING`,
  `RIPPLE_MARTS→LIBRARY_MARTS`. Repo updated to match (database-name refs → `LIBRARY_*`; the `RIPPLE_*`
  env-var *keys* stay — the project is still "Ripple", only the warehouse DBs were rebranded). Verified:
  `SHOW DATABASES` (4 `LIBRARY_*` present, all `RIPPLE*` gone) + `dbt compile` green against the renamed
  stack (compiled SQL resolves to `LIBRARY_RAW.LANDING.*`). `RIPPLE_WH` warehouse unchanged (compute, not a DB).
- Target the live `LIBRARY_*` stack, NOT `DISASTER_IMPACT.RAW`. — Chris, 2026-06-16
- `SOURCE_ID` is the linchpin; landing table = `UPPER(SOURCE_ID)`; prefixes `fed_`/`intl_`/`xc_`/`loc_`/`st_`.
- Catalog is Snowflake-native (`SOURCE_REGISTRY`); raw is an all-TEXT snapshot-replace mirror.
- Compute = `RIPPLE_WH`; the session env leaves `SNOWFLAKE_WAREHOUSE` blank, so the runners self-default it.
- Pin narrow `source_id`s so the upsert inserts a new row instead of clobbering a curated family row.
- Codegen prompt forbids substituting a host/endpoint from memory (the FDIC failure), AND avoids paging
  huge/unbounded sources — fetch a bounded snapshot (the CFPB runaway: it tried to mirror millions of rows).
- dbt builds into `DBT_CROGERS` (not the existing `CORE` schemas); over-strict auto-generated tests on
  real gov data are downgraded to `severity: warn` (Treasury historical nulls, FDA recall-type drift).

## PARKED IDEAS
- [DONE 2026-06-17] Drive the queue from `SOURCE_REGISTRY` (by `PRIORITY_TIER`) instead of the static list.
  → `registry_queue.py` + `registry_batch.py`; proven with `xc_biorxiv_medrxiv`.
- [DONE 2026-06-17 — C2] Incremental load path (append-only landing + watermark + staging dedup). Built in
  `ingest.py`/`recon.py`/prompts; proven live on `fed_cfpb_complaints`. Design: `docs/design-incremental-and-scrape.md`.
- [DONE 2026-06-17 — C1 Phase 1] Static scrape (BS4 + `lxml` + corrected HTML-guard); proven on a Wikipedia
  table (100 rows). Codegen writes good scrape code (BAILII) but most targets are bot-protected/JS-rendered.
- [DONE 2026-06-17 — C1b] Playwright + real browser session for bot-protected / JS-rendered scrape targets.
  → `browser.render()` + `access_pattern=scrape_js` + recon browser-escalation; proven on BAILII UKSC
  (blocked static → 44 judgments rendered). Trade-offs ADR in `docs/design-incremental-and-scrape.md`.
- [IDEA — SOMEDAY] The agent writes a `sources:` block into every model's `schema.yml`; it should emit a
  single central `sources.yml` instead. | NOTE: dbt 1.11 actually tolerates the per-file blocks (parse +
  build are clean) — it only collides if you ALSO add a central one. Cosmetic, not blocking. | LAYER: Library
- [IDEA — SOMEDAY] The agent's generated test YAML trips dbt 1.11 deprecations (generic-test args should
  nest under `arguments:`; `severity` under `config:`). Works now (warnings only), but update the codegen
  prompt before a future dbt makes them errors. | LAYER: Library

## OPEN QUESTIONS
- The PAT authenticates as `ACCOUNTADMIN` — a least-privilege role scoped to `LIBRARY_RAW` + `LIBRARY_META`
  (+ `LIBRARY_STAGING`/`LIBRARY_MARTS` for dbt) would be safer for routine onboarding.

## NEXT ACTION
**C1b — Playwright is built + proven** (BAILII: static blocked → 44 judgments rendered). All three fetch
shapes (bulk/API, static scrape, headless scrape) + both load modes are live. Natural next steps:
**onboard a real `scrape_js` source end-to-end into Snowflake** (e.g. add BAILII UKSC to the registry
queue and run the full agent with live creds — needs a real `ANTHROPIC_API_KEY` + write PAT + warehouse,
which this container didn't have); generate + `dbt run` a staging/mart for `fed_cfpb_complaints`
(dedup-on-`complaint_id`); (D) least-privilege `RIPPLE_INGEST_RW` role; keep feeding the registry queue.
