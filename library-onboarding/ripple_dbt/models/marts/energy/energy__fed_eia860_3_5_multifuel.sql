{{ config(materialized='table', schema='ENERGY') }}

-- Built 2026-08-10 (wave 4). EIA-860 2024 annual report, Schedule 3.5 (Multifuel). Grain: one row = one multi-fuel generator (plant_code + generator_id unique).
-- Reads the typed staging model; grain enforced there and re-tested here.

select * from {{ ref('stg_fed_eia860_3_5_multifuel__all') }}
