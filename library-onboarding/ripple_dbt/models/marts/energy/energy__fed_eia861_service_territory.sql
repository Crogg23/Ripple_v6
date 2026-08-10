{{ config(materialized='table', schema='ENERGY') }}

-- Built 2026-08-10 (backlog wave 4). EIA-861 annual electric utility survey, 2024 vintage.
-- EIA-861 (2024 vintage) Service Territory: counties served by each utility, by state.
-- Grain: surrogate over (data_year, utility_number, state, county).
-- One record is missing: the loader consumed the first data row as the column header.

select * from {{ ref('stg_fed_eia861_service_territory__counties') }}
