# Build State
Last updated: 2026-06-17

## CURRENT FOCUS
Scaling the Library: the onboarding queue is now **registry-driven** (option B). It pulls candidates
straight from the ~900-row `SOURCE_REGISTRY` by `PRIORITY_TIER`, instead of a hand-curated list. Proven
end to end — `xc_biorxiv_medrxiv` was onboarded straight from the catalog, and its registry row flipped
to `INCLUDE=Y` in place (no duplicate). PR #2 + PR #3 (batches 1–3, 12 dbt models) are MERGED to `main`.

## WHAT EXISTS
- `library-onboarding/` — the 5-checkpoint CLI agent: RECON → SCRIPT → LOAD → DBT → REGISTRY.
- LOAD lands raw to `RIPPLE_RAW.LANDING.<UPPER(SOURCE_ID)>` — all columns TEXT, stamped
  `_INGESTED_AT` / `_SOURCE_RUN_ID` / `_SRC_SHA256`, snapshot-replace (idempotent), SHA-256 hash.
- Logs every run to `RIPPLE_META.INGEST_LOGS.INGEST_RUNS`; upserts `RIPPLE_META.REGISTRY.SOURCE_REGISTRY`.
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

**10 clean sources, ~44,965 raw rows.** Registry **901** rows, **13** `INCLUDE=Y` — the false-success
`fed_cms_hpt_enforcement` was dequeued (registry un-flagged + junk table dropped, 2026-06-17, with Chris's OK).
It had landed an HTML page (one `DOCTYPE_HTML` column, 22 junk rows), not data — caught when its mart wouldn't build.

### Registry-driven queue (B) — `xc_biorxiv_medrxiv` (2026-06-17), verified live
- `registry_batch.py --source-id xc_biorxiv_medrxiv --run` selected the row from the catalog and ran the
  full agent. End to end: RECON → LOAD (432 rows → `RIPPLE_RAW.LANDING.XC_BIORXIV_MEDRXIV`) → DBT-gen →
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
  `health__fed_cms_hcris` (6,103) — all materialized into `RIPPLE_MARTS.DBT_CROGERS`.

### Batch 3 — `fed_treasury_avg_interest_rates` (2026-06-17), verified live
- LOAD → `RIPPLE_RAW.LANDING.FED_TREASURY_AVG_INTEREST_RATES` = **4,961 rows**, run `4046bcc7…`,
  sha `7fe37899…` (the same sha is on every row's `_SRC_SHA256` and on the `INGEST_RUNS` row — provenance chain intact).
- `INGEST_RUNS` → one `success` row (4,961 rows, 1.65 MB, ~11s).
- `SOURCE_REGISTRY` → new `INCLUDE=Y` row (Economy / Federal Debt & Interest Rates; join keys
  `record_date, security_type_desc, security_desc`). The curated `fed_fiscaldata_treasury` family row was NOT clobbered.
- Verified independently with the read-only MCP role (`CLAUDE_MCP_READONLY`); the agent wrote via the
  env PAT (`ACCOUNTADMIN`).
- **dbt for batch 3 is RUN** (2026-06-17): `dbt build` created the staging view
  `stg_fed_treasury_avg_interest_rates__avg_interest_rates` (`RIPPLE_STAGING.DBT_CROGERS`) + the mart table
  `economics__fed_treasury_avg_interest_rates` (`RIPPLE_MARTS.DBT_CROGERS`, 4,961 rows, surrogate key 1:1
  unique). Final: **PASS=18, WARN=0, ERROR=0**. One fix: the agent's `accepted_values` on
  `security_type_desc` was wrong (guessed five `Total *` labels from a *different* Treasury dataset) —
  corrected to the 3 real categories `Marketable / Non-marketable / Interest-bearing Debt` (a real guard,
  not downgraded to warn, since the categories are stable + exhaustive across the full history).

- **dbt is RUN** (batches 1–3): all **12 models** (6 sources × staging view + mart table) build into
  `RIPPLE_STAGING.DBT_CROGERS` / `RIPPLE_MARTS.DBT_CROGERS` — 0 errors. (USAspending agencies has no dbt
  models — its first load skipped checkpoint 4.)

## DECISIONS MADE
- Target the live `RIPPLE_*` stack, NOT `DISASTER_IMPACT.RAW`. — Chris, 2026-06-16
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
- [SCOPED 2026-06-17 — C] Scrape + incremental load path for huge/growing/portal sources (CFPB,
  ProPublica, NPPES, per-hospital MRF). Design written: `library-onboarding/docs/design-incremental-and-scrape.md`
  (C2 incremental = append-only landing + watermark + staging dedup; C1 scrape = BS4 then Playwright).
  Recommend building **C2 incremental first**, proven on CFPB complaints. Awaiting foreman go. | LAYER: Library
- [IDEA — SOMEDAY] The agent writes a `sources:` block into every model's `schema.yml`; it should emit a
  single central `sources.yml` instead. | NOTE: dbt 1.11 actually tolerates the per-file blocks (parse +
  build are clean) — it only collides if you ALSO add a central one. Cosmetic, not blocking. | LAYER: Library
- [IDEA — SOMEDAY] The agent's generated test YAML trips dbt 1.11 deprecations (generic-test args should
  nest under `arguments:`; `severity` under `config:`). Works now (warnings only), but update the codegen
  prompt before a future dbt makes them errors. | LAYER: Library

## OPEN QUESTIONS
- The PAT authenticates as `ACCOUNTADMIN` — a least-privilege role scoped to `RIPPLE_RAW` + `RIPPLE_META`
  (+ `RIPPLE_STAGING`/`RIPPLE_MARTS` for dbt) would be safer for routine onboarding.

## NEXT ACTION
**C is scoped** (`docs/design-incremental-and-scrape.md`). Pending foreman go: **build C2 — incremental
load** (`load_mode=incremental` in `ingest.py` + config/recon: append-only landing + watermark + staging
dedup), proven on CFPB consumer complaints. Then C1 scrape (BS4 → Playwright). Other open threads:
(D) least-privilege `RIPPLE_INGEST_RW` role; keep feeding the registry queue at larger limits.
