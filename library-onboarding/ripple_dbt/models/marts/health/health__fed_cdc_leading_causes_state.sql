{{ config(materialized='table', schema='HEALTH') }}

-- Built 2026-08-09: state-geography mortality baselines (NCHS leading causes
-- of death by state, 1999-2017), the state companion to the national-only CDC
-- WONDER grid. Includes a 'United States' rollup row per year x cause.
-- Grain: one row = year x state x cause of death.

select
    year,
    state,
    cause_name,
    icd_113_cause_name,
    deaths,
    age_adjusted_death_rate,
    _ingested_at,
    _source_run_id
from {{ ref('stg_fed_cdc_leading_causes_state__all') }}
