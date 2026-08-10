{{ config(materialized='table', schema='ENERGY') }}

-- Built 2026-08-10 (backlog wave 4). EIA-861 annual electric utility survey, 2024 vintage.
-- EIA-861 (2024 vintage) Utility Data: utility profile with NERC-region flags, RTO/ISO participation flags, and activity flags (generation, transmission, distribution, marketing).
-- Grain: one row per utility per state (UTILITY_NUMBER+STATE is near-unique: 1,699 distinct of 1,701 rows).

select * from {{ ref('stg_fed_eia861_utility_data__utility_profile') }}
