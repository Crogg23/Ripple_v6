# Build State
Last updated: 2026-06-16

## CURRENT FOCUS
Source Onboarding Agent retargeted to the live Ripple v6 warehouse
(`RIPPLE_RAW` / `RIPPLE_META` / `RIPPLE_STAGING` / `RIPPLE_MARTS`).

## WHAT EXISTS
- `library-onboarding/` — the 5-checkpoint CLI agent: RECON → SCRIPT → LOAD → DBT → REGISTRY.
- LOAD lands raw to `RIPPLE_RAW.LANDING.<UPPER(SOURCE_ID)>` — all columns TEXT, stamped
  `_INGESTED_AT` / `_SOURCE_RUN_ID` / `_SRC_SHA256`, snapshot-replace (idempotent),
  SHA-256 content hash, skip-reload-if-unchanged.
- Logs every run to `RIPPLE_META.INGEST_LOGS.INGEST_RUNS`; upserts `RIPPLE_META.REGISTRY.SOURCE_REGISTRY`.
- DBT generation references `source('ripple_raw', <TABLE>)`; staging=view, intermediate (optional),
  mart=table; standard test battery.
- Offline fixture mode (`ONBOARD_FAKE_LLM=1`) runs the whole flow with no API/network/Snowflake.
- Validated: every registry + ingest-log column the agent writes compiles against the live tables;
  full flow runs clean offline.

## DECISIONS MADE
- Target the live `RIPPLE_*` stack, NOT `DISASTER_IMPACT.RAW` (which doesn't exist — that's the
  separate older weather/disaster project). — Chris, 2026-06-16
- `SOURCE_ID` is the linchpin; landing table = `UPPER(SOURCE_ID)`; jurisdiction prefixes
  `fed_`/`intl_`/`xc_`/`loc_`/`st_`.
- Catalog is Snowflake-native (`SOURCE_REGISTRY`); dropped OpenMetadata entirely.
- Raw is an all-TEXT, snapshot-replace mirror (idempotent by construction).

## PARKED IDEAS
- [IDEA — SOMEDAY] Drive the onboarding queue from `SOURCE_REGISTRY` (rows by `INCLUDE` / `PRIORITY_TIER`) instead of the static 37-source `sources_queue.py`. | WHY: ~900 sources already cataloged. | LAYER: Library
- [IDEA — SOMEDAY] Wire `RIPPLE_PRESERVE` vault receipts (`VAULT_RECEIPTS`) into the LOAD step. | WHY: provenance is already half-built. | LAYER: Library

## OPEN QUESTIONS
- `DBT_PROJECT_PATH` not provided yet → DBT checkpoint dry-runs until set.
- Confirm the dbt project's `sources.yml` defines `ripple_raw` (database `RIPPLE_RAW`, schema `LANDING`).
- No real (live-write) run from the agent yet — needs `SNOWFLAKE_PASSWORD` + `SNOWFLAKE_WAREHOUSE`.

## NEXT ACTION
Set `SNOWFLAKE_PASSWORD` + `SNOWFLAKE_WAREHOUSE`, then run one small source end to end to confirm
the live write path (landing + INGEST_RUNS + SOURCE_REGISTRY).
