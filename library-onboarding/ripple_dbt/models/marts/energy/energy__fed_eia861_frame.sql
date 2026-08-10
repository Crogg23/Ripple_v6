{{ config(materialized='table', schema='ENERGY') }}

-- Built 2026-08-10 (backlog wave 4). EIA-861 annual electric utility survey, 2024 vintage.
-- EIA-861 (2024 vintage) Frame: the respondent frame (one row per filing entity) with ownership and fifteen X-marked schedule-participation flags whose header names were destroyed at load (kept positionally as schedule_flag_01..15).
-- Grain: surrogate over (data_year, utility_number).
-- One record is missing: the loader consumed the first data row as the column header.

select * from {{ ref('stg_fed_eia861_frame__respondents') }}
