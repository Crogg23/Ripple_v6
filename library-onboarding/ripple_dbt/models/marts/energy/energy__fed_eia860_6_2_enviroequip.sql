{{ config(materialized='table', schema='ENERGY') }}

-- Built 2026-08-10 (wave 4). EIA-860 2024 annual report, Schedule 6.2 (EnviroEquip). Grain: one row = one boiler (plant_code + boiler_id unique).
-- Reads the typed staging model; grain enforced there and re-tested here.

select * from {{ ref('stg_fed_eia860_6_2_enviroequip__all') }}
