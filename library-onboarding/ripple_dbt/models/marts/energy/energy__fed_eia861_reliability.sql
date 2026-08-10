{{ config(materialized='table', schema='ENERGY') }}

-- Built 2026-08-10 (backlog wave 4). EIA-861 annual electric utility survey, 2024 vintage.
-- EIA-861 (2024 vintage) Reliability: SAIDI/SAIFI/CAIDI outage metrics with and without major event days, under the IEEE standard and the utility's other standard, by utility and state.
-- Grain: surrogate over (data_year, utility_number, state); grain not verifiable pre-clean.

select * from {{ ref('stg_fed_eia861_reliability__reliability_metrics') }}
