{{ config(materialized='table', schema='ENERGY') }}

-- Built 2026-08-10 (backlog wave 4). EIA-861 annual electric utility survey, 2024 vintage.
-- EIA-861 (2024 vintage) Demand Response: enrolled customers, energy savings (MWh), potential and actual peak demand savings (MW), incentives and costs (thousand dollars) by utility, state and sector.
-- Grain: surrogate over (data_year, utility_number, state); grain not verifiable pre-clean.

select * from {{ ref('stg_fed_eia861_demand_response__programs') }}
