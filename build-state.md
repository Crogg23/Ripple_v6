# Build State
Last updated: 2026-06-16

## CURRENT FOCUS
Write path proven AND the full LLM-driven agent is landing real sources into the live
Ripple v6 warehouse (`RIPPLE_RAW` / `RIPPLE_META` / `RIPPLE_STAGING` / `RIPPLE_MARTS`).

## WHAT EXISTS
- `library-onboarding/` — the 5-checkpoint CLI agent: RECON → SCRIPT → LOAD → DBT → REGISTRY.
- LOAD lands raw to `RIPPLE_RAW.LANDING.<UPPER(SOURCE_ID)>` — all columns TEXT, stamped
  `_INGESTED_AT` / `_SOURCE_RUN_ID` / `_SRC_SHA256`, snapshot-replace (idempotent),
  SHA-256 content hash, skip-reload-if-unchanged.
- Logs every run to `RIPPLE_META.INGEST_LOGS.INGEST_RUNS`; upserts `RIPPLE_META.REGISTRY.SOURCE_REGISTRY`.
- DBT generation references `source('ripple_raw', <TABLE>)`; staging=view, intermediate (optional),
  mart=table; standard test battery. A minimal dbt project lives at `library-onboarding/ripple_dbt/`
  (`dbt_project.yml` + `models/staging/sources.yml` defining `ripple_raw`).
- Offline fixture mode (`ONBOARD_FAKE_LLM=1`) runs the whole flow with no API/network/Snowflake.
- **Unattended mode**: `ONBOARD_AUTO_APPROVE=1` auto-"go"s every checkpoint; `ONBOARD_AUTO_REPAIR=N`
  (default 3) feeds a stage error back to Claude and retries before giving up. Foreman can pin a
  `source_id`/`jurisdiction` on the input so a narrow slice doesn't overwrite a broader registry row.

### Live sources onboarded by the agent (2026-06-16)
| SOURCE_ID | rows | how |
|---|---|---|
| `fed_usaspending_toptier_agencies` | 111 | `first_live_load.py` (deterministic) |
| `fed_sec_edgar_company_tickers` | 10,414 | full LLM agent (`live_batch.py`) |
| `fed_federal_register_documents` | 5,000 | full LLM agent (codegen auto-paginated 50×100) |
| `fed_fdic_failed_banks` | 4,115 | full LLM agent (after the URL-hallucination prompt fix) |

Each: a `success` row in `INGEST_RUNS`, an `INCLUDE=Y` row in `SOURCE_REGISTRY` (live Claude
enrichment), and (for the three LLM-driven ones) staging+mart dbt models under `ripple_dbt/models/`.
Registry now 898 rows.
- **dbt is RUN, not just generated** (2026-06-16): `dbt run` built all 6 models — 3 staging views in
  `RIPPLE_STAGING.DBT_CROGERS`, 3 mart tables in `RIPPLE_MARTS.DBT_CROGERS` (SEC 10,414 / FedReg 5,000 /
  FDIC 3,584). `dbt test`: 31/34 pass, 0 errors, 3 warns (FDIC enum drift on charter/agency/resolution
  codes — severity=warn by design). Creds via env (`profiles.yml`, PAT as password); `dbt_utils` pinned.

## DECISIONS MADE
- Target the live `RIPPLE_*` stack, NOT `DISASTER_IMPACT.RAW` (which doesn't exist — that's the
  separate older weather/disaster project). — Chris, 2026-06-16
- `SOURCE_ID` is the linchpin; landing table = `UPPER(SOURCE_ID)`; jurisdiction prefixes
  `fed_`/`intl_`/`xc_`/`loc_`/`st_`.
- Catalog is Snowflake-native (`SOURCE_REGISTRY`); dropped OpenMetadata entirely.
- Raw is an all-TEXT, snapshot-replace mirror (idempotent by construction).
- Compute warehouse is `RIPPLE_WH`. The session env left `SNOWFLAKE_WAREHOUSE` blank, so the
  runners self-default it to `RIPPLE_WH`.
- Pin narrow `source_id`s when onboarding a slice (e.g. `fed_sec_edgar_company_tickers`) so the
  upsert inserts a new row instead of clobbering a curated family row (`fed_sec_edgar`, etc.).
- Codegen prompt now forbids substituting a host/endpoint from memory — must use the exact source
  URL (this was the FDIC failure: the model used `api.fdic.gov` instead of `banks.data.fdic.gov`).
- dbt builds into the `DBT_CROGERS` schema (in `RIPPLE_STAGING` / `RIPPLE_MARTS`) to avoid touching the
  existing `CORE` schemas; dbt auth = PAT-as-password via `env_var` (no secrets committed).

## PARKED IDEAS
- [IDEA — SOMEDAY] Drive the onboarding queue from `SOURCE_REGISTRY` (rows by `INCLUDE` / `PRIORITY_TIER`) instead of the static 37-source `sources_queue.py`. | WHY: ~900 sources already cataloged. | LAYER: Library
- [IDEA — SOMEDAY] Wire `RIPPLE_PRESERVE` vault receipts (`VAULT_RECEIPTS`) into the LOAD step. | WHY: provenance is already half-built. | LAYER: Library

## OPEN QUESTIONS
- The PAT authenticates as `ACCOUNTADMIN` — fine to unblock, but a least-privilege role scoped to
  write only `RIPPLE_RAW` + `RIPPLE_META` would be safer for routine onboarding.
- The agent writes a `sources:` block into every model's `schema.yml`, so a separate central
  `sources.yml` collides (dbt: "two sources with the same name"). Removed the central one for now; the
  agent's dbt generation should emit sources centrally instead. [parked agent fix]

## NEXT ACTION
The 4th source (`fed_usaspending_toptier_agencies`) has no dbt models (its first load skipped
checkpoint 4) — generate + run them, or keep feeding the queue via `live_batch.py`. Optionally tighten
the 3 FDIC `accepted_values` warns (real categories the enum lists missed).
