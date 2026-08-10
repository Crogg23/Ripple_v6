{{ config(materialized='table', schema='HEALTH') }}

-- Built 2026-08-09: national veteran suicide baselines by cohort and year,
-- with optional age-group breakdown. Rows with age_group NULL are the
-- full-cohort series (these carry age-adjusted rates); rows with age_group set
-- come from the by-age sub-tables (no age-adjusted rates published).
-- Grain: one row = year x cohort x age group (age group NULL = full cohort).

select
    year_of_death,
    cohort,
    age_group,
    suicide_deaths,
    population_estimate,
    unadjusted_rate_per_100k,
    age_adjusted_rate_per_100k,
    male_suicide_deaths,
    male_population_estimate,
    male_unadjusted_rate_per_100k,
    male_age_adjusted_rate_per_100k,
    female_suicide_deaths,
    female_population_estimate,
    female_unadjusted_rate_per_100k,
    female_age_adjusted_rate_per_100k,
    _ingested_at,
    _source_run_id
from {{ ref('stg_fed_va_suicide_national__all') }}
