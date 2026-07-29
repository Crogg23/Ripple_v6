{{ config(materialized='table', schema='ENVIRONMENT') }}

-- GRAIN: one row per facility that meets the "penalty gap" criteria
-- Answers: Which facilities have chronic noncompliance but face minimal penalties,
--   and what are the demographics of their surrounding communities?
-- Source: EPA ECHO (filtered to chronic violators with minimal penalties)
-- Key joins: fips_code â†’ geography; facility_name â†’ entity resolution
-- NOTE: This is a MECHANISM mart â€” it reveals the pattern of unenforced environmental harm.

with echo as (
    select * from {{ ref('environment__fed_epa_echo') }}
    where quarters_with_noncompliance >= 4
      and is_active
)

select
    frs_id,
    facility_name,
    city,
    state,
    county,
    fips_code,
    latitude,
    longitude,
    epa_region,
    pct_minority,
    population_density,
    compliance_status,
    quarters_with_noncompliance,
    total_inspection_count,
    formal_action_count,
    total_penalties,
    last_penalty_amt,
    date_last_inspection,
    date_last_formal_action,
    has_air_program,
    has_water_program,
    has_hazwaste_program,
    tri_on_site_releases,

    -- Derived disparity flags
    (total_penalties < 1000 and quarters_with_noncompliance >= 8) as chronic_no_penalty,
    (pct_minority >= 50) as in_majority_minority_community,
    (total_inspection_count = 0 and quarters_with_noncompliance >= 4) as never_inspected_noncompliant,
    round(total_penalties / nullif(quarters_with_noncompliance, 0), 2) as penalty_per_quarter_nc,

    _loaded_at,
    _source_run_id
from echo
