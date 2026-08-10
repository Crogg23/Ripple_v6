{{ config(materialized='table', schema='FINANCE') }}

-- Built 2026-08-10 (backlog wave 4). OCC-chartered national banks; cert joins to FDIC data, rssd joins to Federal Reserve / FFIEC data.
-- Grain: one row = one OCC-chartered national bank (charter_no unique). Reads the staging model built alongside it.

select * from {{ ref('stg_fed_occ_national_banks__banks') }}
