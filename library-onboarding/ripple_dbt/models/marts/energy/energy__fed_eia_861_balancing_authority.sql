{{ config(materialized='table', schema='ENERGY') }}

-- Built 2026-08-10 (wave 4). EIA-861 2024 annual report, Balancing Authority sheet. Grain: one row = one balancing authority x state (ba_id + state unique).
-- Reads the typed staging model; grain enforced there and re-tested here.

select * from {{ ref('stg_fed_eia_861_balancing_authority__all') }}
