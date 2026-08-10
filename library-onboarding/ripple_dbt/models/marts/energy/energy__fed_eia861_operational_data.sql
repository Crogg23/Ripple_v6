{{ config(materialized='table', schema='ENERGY') }}

-- Built 2026-08-10 (backlog wave 4). EIA-861 annual electric utility survey, 2024 vintage.
-- EIA-861 (2024 vintage) Operational Data: peak demand (MW), energy sources and disposition (MWh), and revenue (thousand dollars) by utility and state.
-- Grain: surrogate over (data_year, utility_number, state); grain not verifiable pre-clean.

select * from {{ ref('stg_fed_eia861_operational_data__operations') }}
