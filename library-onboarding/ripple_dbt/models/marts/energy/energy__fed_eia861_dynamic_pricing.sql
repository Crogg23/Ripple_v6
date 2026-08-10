{{ config(materialized='table', schema='ENERGY') }}

-- Built 2026-08-10 (backlog wave 4). EIA-861 annual electric utility survey, 2024 vintage.
-- EIA-861 (2024 vintage) Dynamic Pricing: customers enrolled in dynamic-rate programs and Y/N program flags (time-of-use, real-time, variable-peak, critical-peak pricing/rebate) by utility, state and sector.
-- Grain: surrogate over (data_year, utility_number, state); grain not verifiable pre-clean.

select * from {{ ref('stg_fed_eia861_dynamic_pricing__enrollment') }}
