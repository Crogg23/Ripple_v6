{{ config(materialized='table', schema='IMMIGRATION') }}

-- Built 2026-08-09 (73-source backlog). ICE detainers Oct 2022-2026,
-- person-level (anonymized hashes). Kept as landed including the
-- duplicate_likely flag (blank on ~75k rows) — rows are only unique with
-- file+row provenance, so no dedup is attempted here.
-- Grain: one row = one detainer record as published.

select * from {{ ref('stg_fed_ice_detainers__all') }}
