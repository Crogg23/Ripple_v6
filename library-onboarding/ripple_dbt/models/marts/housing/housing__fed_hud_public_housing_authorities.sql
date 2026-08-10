{{ config(materialized='table', schema='HOUSING') }}

-- Built 2026-08-10 (backlog wave 4). HUD Public Housing Authorities: one row
-- per PHA (participant_code unique) with unit counts, occupancy, operating /
-- capital funding, per-PHA resident demographics, and geocoded address.
-- Grain: one row = one public housing authority. Reads the staging model.

select * from {{ ref('stg_fed_hud_public_housing_authorities__authorities') }}
