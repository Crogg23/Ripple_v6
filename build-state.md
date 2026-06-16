# Build State
Last updated: 2026-06-16

## CURRENT FOCUS
First live load is DONE — the onboarding agent's write path is proven against the
live Ripple v6 warehouse (`RIPPLE_RAW` / `RIPPLE_META` / `RIPPLE_STAGING` / `RIPPLE_MARTS`).

## WHAT EXISTS
- `library-onboarding/` — the 5-checkpoint CLI agent: RECON → SCRIPT → LOAD → DBT → REGISTRY.
- LOAD lands raw to `RIPPLE_RAW.LANDING.<UPPER(SOURCE_ID)>` — all columns TEXT, stamped
  `_INGESTED_AT` / `_SOURCE_RUN_ID` / `_SRC_SHA256`, snapshot-replace (idempotent),
  SHA-256 content hash, skip-reload-if-unchanged.
- Logs every run to `RIPPLE_META.INGEST_LOGS.INGEST_RUNS`; upserts `RIPPLE_META.REGISTRY.SOURCE_REGISTRY`.
- DBT generation references `source('ripple_raw', <TABLE>)`; staging=view, intermediate (optional),
  mart=table; standard test battery.
- Offline fixture mode (`ONBOARD_FAKE_LLM=1`) runs the whole flow with no API/network/Snowflake.
- **FIRST LIVE LOAD (2026-06-16):** `fed_usaspending_toptier_agencies` — USAspending top-tier federal
  agencies, 111 rows → `RIPPLE_RAW.LANDING.FED_USASPENDING_TOPTIER_AGENCIES`; one `success` row in
  `INGEST_RUNS` (52,673 bytes, sha `d8f46b61…`); registry row inserted (894 → 895), `INCLUDE=Y`, with
  live Claude catalog enrichment (`EPSTEIN_RELEVANT=maybe` + relevance/notes). Driven by
  `library-onboarding/first_live_load.py`, which calls the agent's real `run_ingest()` + `register_source()`.
- Validated end to end: all three network paths work from a fresh session — Snowflake (PAT → role
  `ACCOUNTADMIN`, warehouse `RIPPLE_WH`), source egress (USAspending), and Anthropic API (`api.anthropic.com`).

## DECISIONS MADE
- Target the live `RIPPLE_*` stack, NOT `DISASTER_IMPACT.RAW` (which doesn't exist — that's the
  separate older weather/disaster project). — Chris, 2026-06-16
- `SOURCE_ID` is the linchpin; landing table = `UPPER(SOURCE_ID)`; jurisdiction prefixes
  `fed_`/`intl_`/`xc_`/`loc_`/`st_`.
- Catalog is Snowflake-native (`SOURCE_REGISTRY`); dropped OpenMetadata entirely.
- Raw is an all-TEXT, snapshot-replace mirror (idempotent by construction).
- Compute warehouse is `RIPPLE_WH` (X-Small, auto-suspend 60s). The session env left
  `SNOWFLAKE_WAREHOUSE` blank, so `first_live_load.py` self-defaults it to `RIPPLE_WH`.
- First live load is deterministic on purpose — hand-built config + `fetch_data`, not Claude recon/codegen.
  The LLM path is wired and reachable; we just wanted the first *write* to be predictable.

## PARKED IDEAS
- [IDEA — SOMEDAY] Drive the onboarding queue from `SOURCE_REGISTRY` (rows by `INCLUDE` / `PRIORITY_TIER`) instead of the static 37-source `sources_queue.py`. | WHY: ~900 sources already cataloged. | LAYER: Library
- [IDEA — SOMEDAY] Wire `RIPPLE_PRESERVE` vault receipts (`VAULT_RECEIPTS`) into the LOAD step. | WHY: provenance is already half-built. | LAYER: Library

## OPEN QUESTIONS
- The PAT authenticates as `ACCOUNTADMIN` — fine to unblock, but a least-privilege role scoped to write
  only `RIPPLE_RAW` + `RIPPLE_META` would be safer for routine onboarding.
- `DBT_PROJECT_PATH` not provided yet → DBT checkpoint (4) still dry-runs/aborts until set. First live
  load deliberately skipped DBT (the ask was LANDING + INGEST_RUNS + SOURCE_REGISTRY).
- Confirm the dbt project's `sources.yml` defines `ripple_raw` (database `RIPPLE_RAW`, schema `LANDING`).

## NEXT ACTION
Run the full LLM-driven `onboard.py` against a real source now that the write path is proven — either
wire `DBT_PROJECT_PATH` so all 5 checkpoints complete, or run RECON → SCRIPT → LOAD → REGISTRY and skip DBT.
