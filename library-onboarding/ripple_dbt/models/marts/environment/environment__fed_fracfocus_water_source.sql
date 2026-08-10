{{ config(materialized='table', schema='ENVIRONMENT') }}

-- Built 2026-08-10 (73-source backlog, wave 3). FracFocus water sources —
-- where the base water for each fracking job came from (23,747 rows).
-- Grain: one row = one water source line within a well disclosure
-- (water_source_id unique).

select * from {{ ref('stg_fed_fracfocus_water_source__water_sources') }}
