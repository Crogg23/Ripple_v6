{{ config(materialized='table', schema='ENERGY') }}

-- Built 2026-08-10 (backlog wave 4). EIA-861 annual electric utility survey, 2024 vintage.
-- EIA-861 (2024 vintage) Short Form: total revenue (thousand dollars), sales (MWh) and customers for short-form respondents; the last four columns' header names were destroyed at load and are kept positionally as unrecovered_*.
-- Grain: surrogate over (data_year, utility_number, state).
-- One record is missing: the loader consumed the first data row as the column header.

select * from {{ ref('stg_fed_eia861_short_form__responses') }}
