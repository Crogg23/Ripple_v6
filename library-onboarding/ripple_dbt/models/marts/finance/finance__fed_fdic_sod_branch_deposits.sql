{{ config(materialized='table', schema='FINANCE') }}

-- Built 2026-08-10 (backlog wave 4). FDIC Summary of Deposits: FULL survey
-- history 1994-2025, ~2.82M rows -- every FDIC-insured bank branch and its
-- deposits, each survey year, with parent-institution and holding-company
-- context plus SIMS geocoding.
-- Grain: one row = one branch in one survey year (YEAR + CERT + BRNUM,
-- verified unique; branch_year_key concatenates them).
-- Join keys: fdic_cert (FDIC institution directory), rssd_id and
-- holding_company_rssd (Fed NIC / FFIEC bank registries).

select * from {{ ref('stg_fed_fdic_sod_branch_deposits__branches') }}
