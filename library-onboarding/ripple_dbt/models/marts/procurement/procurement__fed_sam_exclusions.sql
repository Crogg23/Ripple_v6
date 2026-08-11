{{ config(materialized='table', schema='PROCUREMENT') }}

-- GRAIN: one row per exclusion record (sam_number — unique in the source file).
-- Answers: Who has been debarred/suspended from federal contracting, and for how long?
-- Source: SAM.gov Exclusions, re-pulled in full 2026-08-11 — 167,928 rows
-- (old capped table held ~9K). NOTE the grain change from the capped era: the
-- full file carries multiple exclusion records per entity, so UEI is NOT unique
-- here and the mart no longer dedupes on it. TERMINATION_DATE is the literal
-- text 'Indefinite' on ~95% of rows — those parse to NULL dates and count as
-- currently excluded.
-- Key joins: entity_name/cage -> USAspending contracts; npi -> health providers

with base as (
    select * from {{ ref('stg_fed_sam_exclusions__records') }}
)

select
    sam_number,
    uei,
    cage                                           as cage_code,
    npi,
    entity_name,
    first_name,
    last_name,
    classification,
    exclusion_type,
    exclusion_program,
    excluding_agency,
    try_to_date(activation_date, 'YYYY-MM-DD')     as activation_date,
    termination_date                               as termination_date_raw,
    try_to_date(termination_date, 'YYYY-MM-DD')    as termination_date,
    record_status,
    city,
    state,
    zip,
    country,
    coalesce(
        termination_date is null
        or upper(termination_date) = 'INDEFINITE'
        or try_to_date(termination_date, 'YYYY-MM-DD') > current_date(),
        true)                                      as is_currently_excluded,
    (entity_name is not null and last_name is null) as is_entity_not_individual,
    _loaded_at
from base
qualify row_number() over (
    partition by sam_number
    order by _loaded_at desc
) = 1
