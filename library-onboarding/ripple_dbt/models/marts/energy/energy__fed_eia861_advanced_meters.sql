{{ config(materialized='table', schema='ENERGY') }}

-- Built 2026-08-10 (backlog wave 4). EIA-861 annual electric utility survey, 2024 vintage.
-- EIA-861 (2024 vintage) Advanced Meters: AMR/AMI meter counts and energy served through AMI, by utility, state, and customer sector.
-- Grain: one row per utility per state (UTILITY_NUMBER+STATE is near-unique: 2,683 distinct of 2,725 rows).

select * from {{ ref('stg_fed_eia861_advanced_meters__meter_counts') }}
