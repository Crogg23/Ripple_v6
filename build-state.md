# Build State
Last updated: 2026-06-16

## CURRENT FOCUS
Growing the Library via the full LLM agent. PR #2 (retarget + first loads + dbt) is MERGED;
batch-2 sources land on `claude/reconcile-onboarding-agent` (no PR opened yet post-merge).

## WHAT EXISTS
- `library-onboarding/` — the 5-checkpoint CLI agent: RECON → SCRIPT → LOAD → DBT → REGISTRY.
- LOAD lands raw to `RIPPLE_RAW.LANDING.<UPPER(SOURCE_ID)>` — all columns TEXT, stamped
  `_INGESTED_AT` / `_SOURCE_RUN_ID` / `_SRC_SHA256`, snapshot-replace (idempotent), SHA-256 hash.
- Logs every run to `RIPPLE_META.INGEST_LOGS.INGEST_RUNS`; upserts `RIPPLE_META.REGISTRY.SOURCE_REGISTRY`.
- **Unattended**: `ONBOARD_AUTO_APPROVE=1` + `ONBOARD_AUTO_REPAIR=N` (default 3, feeds errors back to
  Claude). `live_batch.py` is the canonical growing queue — skips anything already landed, safe to re-run.
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

6 sources, ~32,969 raw rows. Registry now **900** rows. Each: a `success` row in `INGEST_RUNS`, an
`INCLUDE=Y` row in `SOURCE_REGISTRY` (live Claude enrichment).

- **dbt is RUN**: `dbt run` builds all **10 models** (5 sources × staging view + mart table) into
  `RIPPLE_STAGING.DBT_CROGERS` / `RIPPLE_MARTS.DBT_CROGERS` — 0 errors. `dbt test`: **PASS=60, WARN=13,
  ERROR=0**. (USAspending agencies has no dbt models — its first load skipped checkpoint 4.)

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
- [IDEA — SOMEDAY] Drive the queue from `SOURCE_REGISTRY` (by `INCLUDE`/`PRIORITY_TIER`) instead of the static list. | WHY: ~900 sources cataloged. | LAYER: Library
- [IDEA — HOT] CFPB complaints + ProPublica nonprofits are huge, daily-growing search APIs — a snapshot
  mirror is the wrong shape. Need an **incremental** load path before onboarding them. | LAYER: Library
- [IDEA — SOMEDAY] The agent writes a `sources:` block into every model's `schema.yml`; it should emit a
  single central `sources.yml` instead (avoids duplicate-source conflicts). | LAYER: Library

## OPEN QUESTIONS
- The PAT authenticates as `ACCOUNTADMIN` — a least-privilege role scoped to `RIPPLE_RAW` + `RIPPLE_META`
  (+ `RIPPLE_STAGING`/`RIPPLE_MARTS` for dbt) would be safer for routine onboarding.

## NEXT ACTION
PR #2 merged mid-batch — decide how batch-2 work (Treasury + FDA + dbt) lands: new PR, or fold into the
next one. Then keep feeding the queue via `live_batch.py`, and build the incremental path for CFPB-style sources.
