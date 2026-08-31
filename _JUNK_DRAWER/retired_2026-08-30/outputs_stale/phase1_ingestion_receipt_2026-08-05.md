# Phase 1 ingestion receipt — 2026-08-05

Landed via scripts/*.py (small_flat_loader / cisa_kev pattern), registered in
SOURCE_REGISTRY, staging models generated with generate_staging_models.py.
`dbt build`/`dbt test` currently blocked repo-wide by dbt-fusion 2.0-preview
deprecated test-syntax errors (pre-existing, not introduced tonight) — verified
manually in Snowflake instead (row counts, COUNT DISTINCT keys, TRY_TO_DATE).

| Source | Table | Rows | Key verified |
|---|---|---|---|
| JPML Pending MDLs | FED_JPML_PENDING_MDL | 161 | MDL_NUMBER 161/161 distinct |
| FHFA Suspended Counterparty | FED_FHFA_SUSPENDED_COUNTERPARTY | 241 | matches site's stated 241; composite key 231/241 distinct (some re-listed people) |
| ICE detention facility codes | FED_ICE_DETENTION_FACILITY_CODES | 1,490 | DETENTION_FACILITY_CODE 1490/1490 distinct; no person-level columns |
| Consolidated Screening List | FED_CONSOLIDATED_SCREENING_LIST | 25,918 | ID+SOURCE 25918/25918 distinct |
| OEHHA Prop 65 | STATE_OEHHA_PROP65_CHEMICALS | 1,021 | landed by my loader |
| UN Consolidated Sanctions | INTL_UN_CONSOLIDATED_SANCTIONS | 1,011 | landed by my loader |
| UK Sanctions List | INTL_UK_SANCTIONS_LIST | 57,883 | landed by my loader |
| VAERS | -- | 0 | BLOCKED -- see below |

## Anomaly found, not caused by tonight's work
While generating staging models, found pre-existing landing tables + staging
models for the same 3 sources under different names/IDs, created within
minutes of my own loads tonight:
- `ST_OEHHA_PROPOSITION_65_LIST` (1,021 rows)
- `XC_UK_SANCTIONS_LIST` (57,883 rows)
- `XC_UN_CONSOLIDATED_SANCTIONS_LIST` (1,011 rows)

Row counts match mine almost exactly; timestamps are minutes apart. Not from
`RIPPLE_BULK_REFRESH_TASK` (checked -- none of those 3 sources are in
`BULK_REFRESH`, and all its rows are ENABLED=FALSE). Likely a concurrent
session/agent working the same plan at the same time. Did not delete anything
on either side -- flagging for Chris to pick a canonical copy and dedupe.

## New trap found
VAERS (vaers.hhs.gov) requires solving an image CAPTCHA before any file --
yearly zips and the AllVAERSDataCSVS.zip bulk file -- will serve. Not on the
known-trap list. No CAPTCHA-free mirror found this session (healthdata.gov's
VAERS/WONDER Socrata resource returned "no row or column access to
non-tabular tables"). Did not fight it; marked blocked.
