{{ config(materialized='table', schema='HOUSING') }}

-- Built 2026-08-09 (73-source backlog, wave 2c). HUD Picture of Subsidized Households: assisted-housing units and tenant profiles by project/program/geography. NEGATIVE values are HUD suppression/N-A sentinels (kept as published -- filter value >= 0 for analysis).
-- Grain: one row = one quarter x summary-level x program x code (verified unique).

select * from {{ ref('stg_fed_hud_assisted_housing_projects__summaries') }}
