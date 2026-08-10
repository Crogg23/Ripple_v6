{{ config(materialized='table', schema='HEALTH') }}

-- Built 2026-08-09: veteran suicide by state, from the by-state sheet of the
-- VA appendix (the staging model stacks four sheets; the sheet column gates
-- which dimensions are populated, so this filters to the state sheet only —
-- sex/age/method breakdowns are national-only and live in
-- health__fed_va_suicide_national and the staging model).
-- Grain: one row = year x state. Suppressed cells are NULL.

select
    year_of_death,
    geographic_region,
    state,
    veteran_suicides,
    population_estimate                as veteran_population_estimate,
    veteran_suicide_rate_per_100k,
    general_population_suicides,
    general_population_rate_per_100k,
    _ingested_at,
    _source_run_id
from {{ ref('stg_fed_va_suicide_state__all') }}
where sheet = 'Veteran Suicides by State'
