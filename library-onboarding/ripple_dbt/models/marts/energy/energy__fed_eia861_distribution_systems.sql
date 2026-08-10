{{ config(materialized='table', schema='ENERGY') }}

-- Built 2026-08-10 (backlog wave 4). EIA-861 annual electric utility survey, 2024 vintage.
-- EIA-861 (2024 vintage) Distribution Systems: number of distribution circuits and circuits with voltage optimization by utility and state.
-- Grain: surrogate over (data_year, utility_number, state).
-- One record is missing: the loader consumed the first data row as the column header.

select * from {{ ref('stg_fed_eia861_distribution_systems__circuits') }}
