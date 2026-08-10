{{ config(materialized='table', schema='ENERGY') }}

-- Built 2026-08-10 (wave 4). EIA-860 2024 annual report, Schedule 1 (Utility). Grain: one row = one utility (utility_id unique).
-- Reads the typed staging model; grain enforced there and re-tested here.

select * from {{ ref('stg_fed_eia860_1_utility__all') }}
