{{ config(materialized='table', schema='ENVIRONMENT') }}

-- Built 2026-08-10 (73-source backlog, wave 3). EPA Facility Registry Service
-- national facility file (3.28M rows). Grain: one row = one facility
-- (registry_id unique). A larger FRS extract (FED_EPA_FRS_FULL, ~5.3M) is
-- modeled separately, but 84,926 registry IDs here are NOT in that extract
-- (verified 2026-08-10) — different vintages/cuts, both kept.

select * from {{ ref('stg_fed_epa_frs_frs_facilities__facilities') }}
