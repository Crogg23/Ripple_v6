# Build State
Last updated: 2026-06-17

## CURRENT FOCUS
The agent now has **three fetch capabilities** and picks each autonomously at recon: **bulk/API**,
**static scrape** (C1, BS4), and **headless-browser scrape** (C1b, Playwright `render()` for
JS-rendered / bot-protected pages) — plus two **load modes** (snapshot + C2 incremental). C1b is now
**proven full end-to-end through `onboard.py` with real creds**: recon autonomously set `scrape_js`,
codegen used the injected `render()`, Playwright cleared a JS shell, and 100 rows landed in
`LIBRARY_RAW.LANDING` + registered in `LIBRARY_META` (target `quotes.toscrape.com/js` — BAILII's wall was
down at run time; see the C1b end-to-end section for why). With full capability proven, **ran registry
batches 2 + 3** (tier-1, auth-free): batch 2 = 12 attempted → 4 landed (incl. FARA 221,900); batch 3 = 4
ran before an **Anthropic credit exhaustion** halted the queue → 3 landed (incl. Mapping Inequality 10,154),
8 credit-blocked (still queued for retry). **Live total: 26 landing tables, 1,956,308 rows.** PR #2–#8
merged to `main`; batch-3 work is on `claude/laughing-knuth-fmjka8`. **Blocked on: Anthropic API credits.**

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
| `fed_cms_nursing_home` | 14,700 | **registry batch 2** (2026-06-17 — bulk CSV, Care Compare) |
| `fed_doj_fca_settlements` | 19 | registry batch 2 (DOJ False Claims Act press-release scrape) |
| `fed_doj_crt_cases` | 1 | registry batch 2 (DOJ Civil Rights portal scrape — ⚠ thin/incomplete, review) |
| `fed_fara_bulk` | 221,900 | registry batch 2 (FARA eFile bulk — foreign-agent registrations) |
| `fed_mapping_inequality` | 10,154 | **registry batch 3** (2026-06-17 — HOLC redlining, GeoJSON flattened to rows) |
| `fed_hhs_taggs` | 45 | registry batch 3 (HHS grant-tracking, incremental backfill) |
| `fed_fdic_enforcement` | 2 | registry batch 3 (FDIC enforcement portal scrape — ⚠ thin, review) |

**18 clean sources in `LANDING`** (batch 2 +4, batch 3 +3). Live total: **26 landing tables,
1,956,308 raw rows** (was 19 / 1,709,487 before batch 2; batch 3 added +10,201). The demo `intl_demo_quotes_toscrape_js`
was dropped (table + registry + ingest_runs) before the batch. The false-success `fed_cms_hpt_enforcement`
was dequeued earlier (registry un-flagged + junk table dropped, 2026-06-17, with Chris's OK): it had landed
an HTML page (one `DOCTYPE_HTML` column, 22 junk rows), not data — caught when its mart wouldn't build.

### Registry batch 2 — `registry_batch.py` tier-1, auth-free, per-source timeout (2026-06-17)
Ran the queue end to end through the full agent (all 4 fetch capabilities live), each source wrapped in a
12-min wall-clock `timeout` so one hang couldn't stall the session. **12 attempted, 4 landed, 1 false-success
(corrected), 7 failed.** The easy bulk/API sources were already onboarded — this tier-1 residue is the hard
portal/scrape/huge shapes, so a low hit-rate is expected.

| Source | Result | Rows |
|---|---|---|
| `fed_cms_nursing_home` | ✅ onboarded | 14,700 |
| `fed_doj_fca_settlements` | ✅ onboarded (press-release scrape) | 19 |
| `fed_doj_crt_cases` | ✅ onboarded — ⚠ **thin scrape, review** | 1 |
| `fed_fara_bulk` | ✅ onboarded (bulk) | 221,900 |
| `fed_cms_tic_mrf` | ⚠ **false success → un-flagged** (incremental first-run 0 rows, no table) | 0 |
| `fed_chronicling_america` | ❌ aborted — LoC API migrated/dead (404) | — |
| `fed_cms_hpt_mrf` | ❌ aborted — per-hospital MRF crawl, no single data file | — |
| `fed_cms_ma_enrollment` | ❌ aborted — CMS dynamic portal, grabbed instructions ZIP / no CSV links | — |
| `fed_cms_nppes` | ❌ killed (exit 137, OOM) — ~9 GB download blew container memory | — |
| `fed_densho_ddr` | ❌ aborted — portal-only, no machine-readable endpoint | — |
| `fed_docsouth` | ❌ aborted — couldn't resolve a bulk data file | — |
| `fed_epa_egrid` | ❌ aborted — multi-sheet Excel / dynamic download | — |

- **Agent gap this exposed + FIXED**: an **incremental** source whose **first** run (empty watermark, `since
  is None`) returns 0 rows was logged `success` (0 rows) and flipped `INCLUDE=Y` — a false success with no
  table (`fed_cms_tic_mrf`: recon called the per-insurer MRF incremental, the scrape found nothing). Fix in
  `ingest.run_ingest`: `allow_empty` now only applies to a *continuing* incremental run (`since is not None`);
  a first-run empty backfill fails loudly (→ auto-repair → abort), so it can't false-succeed. tic_mrf's
  registry row was un-flagged (`INCLUDE` blank); the 0-row `INGEST_RUNS` record is kept as history.
- **Also seen (not yet fixed)**: codegen occasionally emits a prose preamble before the code block →
  `extract_code` returns it → `invalid syntax (line 1)`; it self-corrected on retry here. Worth hardening
  `extract_code`/the codegen system prompt before a future batch. The DOJ CRT 1-row landing is a thin-scrape
  near-miss (no pagination) — flagged for review, not auto-dequeued (it did land structured data).

### Registry batch 3 — next 12 fresh tier-1 (skipping batch-2's 8 attempts), 2026-06-17
Worked further down the queue, excluding the 8 sources batch 2 already attempted. **Cut short by an
Anthropic API credit exhaustion partway through** — so the run splits in two:
- **Ran with working credits (4):** `fed_mapping_inequality` ✅ 10,154 (GeoJSON flattened), `fed_hhs_taggs`
  ✅ 45, `fed_fdic_enforcement` ✅ 2 (⚠ thin portal scrape), `fed_fjc_idb` ❌ killed (OOM — large bulk CSV).
- **Credit-blocked (8, NOT genuine failures — still queued for retry):** `fed_mapping_prejudice`,
  `fed_naag_multistate_settlements`, `fed_nara_aad`, `fed_nara_wra_aad`, `fed_noaa_ais`, `fed_npdb_puf`,
  `fed_olms_lm_reports`, `fed_opm_fedworkforce` — every `call_claude` returned HTTP 400 "credit balance is
  too low", so recon couldn't run and each aborted in ~6s. These left zero partial state (no landing, no
  `INGEST_RUNS`, registry untouched) — re-run them once credits are topped up.
- **BLOCKER surfaced (stopped the queue):** the `ANTHROPIC_API_KEY` has no credits left. No further batches
  can run until it's funded — this is the pipeline-wide stop condition, not source difficulty.
- **Recurring OOM on big bulk files** (`fed_cms_nppes` ~9 GB in batch 2, `fed_fjc_idb` in batch 3): the load
  path reads the whole download into pandas in memory → container OOM (exit 137). Follow-up: stream/chunk
  large downloads (or cap rows) so multi-GB sources don't get killed.

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
- **NOTE on the C1b PR container**: that earlier proof exercised the full RECON→SCRIPT→LOAD-*fetch* path
  (render injection + generated `fetch_data` + HTML-junk guard). The Snowflake **write** + real-LLM codegen
  weren't run there (placeholder creds). Now done — see below.

### C1b — FULL end-to-end live proof through `onboard.py` (2026-06-17, real creds)
Ran the whole agent (`onboard.py --url …`, `ONBOARD_AUTO_APPROVE=1`) with a real `ANTHROPIC_API_KEY` +
write PAT (`ACCOUNTADMIN`) + `DBT_WH`, browser at `/opt/pw-browsers`. All 5 checkpoints green, exit 0:
- **RECON → `access_pattern=scrape_js` autonomously**, **codegen wrote `context["render"](url,
  wait_selector=".quote")`**, Playwright cleared the JS shell, **LOAD landed 100 rows** →
  `LIBRARY_RAW.LANDING.INTL_DEMO_QUOTES_TOSCRAPE_JS` with full provenance (`_INGESTED_AT` /
  `_SOURCE_RUN_ID` / `_SRC_SHA256`), one `success` row in `INGEST_RUNS` (100 rows, 93,596 B, sha
  `03c989fc4da3`), and a `SOURCE_REGISTRY` row (`INCLUDE=Y`). Verified independently via the read-only
  MCP role. DBT checkpoint also ran (demo models written, not committed — see target note).

**Target = `quotes.toscrape.com/js` (a JS-render sandbox), NOT BAILII — and why:**
- **BAILII's bot wall is intermittent / IP-reputation-based.** At run time it served the *real* page to a
  plain `requests` GET (12 KB, 0 challenge markers) — so recon *correctly* called it plain `scrape`, and a
  scrape_js proof on it would've been theatre. (This is exactly the "fragile / arms-race" trade-off in the
  ADR.) BAILII still works via static scrape right now; it just isn't a JS wall *today from this IP*.
- Swept the queue's real JS candidates: **OECD** data-explorer is a true JS shell (0 visible chars static)
  but headless render returns an SPA *error* page (needs bespoke UI-driving); **ICIJ**/`pages/database`,
  OpenSanctions, GDELT, GFW, supremecourt.uk are all server-rendered (real content static → plain scrape).
  None cleanly exercises scrape_js from a single URL. `quotes.toscrape.com/js` reliably does: static = 0
  data rows (JS shell), render = real quotes. Registered with NOTES flagging it a demo to exclude from
  real analysis. **It can be dropped on request** (`DROP TABLE LIBRARY_RAW.LANDING.INTL_DEMO_QUOTES_TOSCRAPE_JS`
  + delete its `SOURCE_REGISTRY` / `INGEST_RUNS` rows).

**Autonomy hardening this exposed (committed):** recon was picking `scrape` even for JS shells because it
*escalates to the browser to read walled pages*, so the LLM saw clean rendered HTML and mislabeled it. Fixes:
(1) `browser.looks_blocked` now judges **visible text** (a JS SPA shell is 100+ KB of HTML with ~0 visible
chars — the old raw-byte-length test missed it); (2) `recon.fetch_page` returns a `browser_required` signal
(static was blocked, only render worked); (3) `recon._resolve` **forces `access_pattern=scrape_js` on that
empirical signal** rather than trusting the LLM. Deterministic across repeated runs after the fix.

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
