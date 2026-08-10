{{ config(materialized='table', schema='ENVIRONMENT') }}

-- Built 2026-08-10 (backlog wave 3). EPA RCRAInfo handler NAICS industry codes: one row = one handler-location-NAICS link (exactly unique).
-- Reads the grain-verified staging model.

select * from {{ ref('stg_fed_epa_rcra_rcra_naics__naics_codes') }}
