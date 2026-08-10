{{ config(materialized='table', schema='ENERGY') }}

-- Built 2026-08-10 (wave 4). EIA-860 2024 annual report, Schedule 4 (Owner). Grain: one row = one owner stake in a generator (plant_code + generator_id + ownership_id unique).
-- Reads the typed staging model; grain enforced there and re-tested here.

select * from {{ ref('stg_fed_eia860_4_owner__all') }}
