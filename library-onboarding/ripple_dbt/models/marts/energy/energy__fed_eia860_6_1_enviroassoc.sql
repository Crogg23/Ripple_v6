{{ config(materialized='table', schema='ENERGY') }}

-- Built 2026-08-10 (wave 4). EIA-860 2024 annual report, Schedule 6.1 (EnviroAssoc). Grain: one row = one boiler-generator association (plant_code + boiler_id + generator_id + steam_plant_type unique).
-- Reads the typed staging model; grain enforced there and re-tested here.

select * from {{ ref('stg_fed_eia860_6_1_enviroassoc__all') }}
