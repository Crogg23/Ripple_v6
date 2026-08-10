{{ config(materialized='table', schema='HEALTH') }}

-- Rewritten 2026-08-09: the old version read the broken PDF-scrape landing shape
-- (FIGURES_AND_TABLES/COL_n, 244 junk rows) straight from raw. The source was
-- relanded from the official xlsx appendix; this now builds on the real staging
-- model. Grain: one row = cohort x sex x year x cause of death.

select
    year,
    cohort,
    sex,
    cause_of_death,
    rank,
    deaths,
    percent_of_deaths,
    unadjusted_rate,
    age_adjusted_rate,
    crude_rate,
    ypll,
    ypll_pct,
    _ingested_at,
    _source_run_id
from {{ ref('stg_fed_va_allcause_mortality__all') }}
