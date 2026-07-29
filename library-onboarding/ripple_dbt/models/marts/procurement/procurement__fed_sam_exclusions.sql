{{ config(materialized='table', schema='PROCUREMENT') }}

-- GRAIN: one row per excluded entity (UEI or entity_name + activation_date)
-- Answers: Who has been debarred/suspended from federal contracting, and for how long?
-- Source: SAM.gov Exclusions (~9K records)
-- Key joins: entity_name/cage â†’ USAspending contracts; npi â†’ health providers

with base as (
    select * from {{ ref('stg_fed_sam_exclusions__records') }}
)

select
    trim(uei)                                      as uei,
    trim(cage)                                     as cage_code,
    trim(npi)                                      as npi,
    trim(entity_name)                              as entity_name,
    trim(first_name)                               as first_name,
    trim(last_name)                                as last_name,
    trim(classification)                           as classification,
    trim(exclusion_type)                           as exclusion_type,
    trim(exclusion_program)                        as exclusion_program,
    trim(excluding_agency)                         as excluding_agency,
    try_to_date(activation_date, 'YYYY-MM-DD')     as activation_date,
    try_to_date(termination_date, 'YYYY-MM-DD')    as termination_date,
    trim(record_status)                            as record_status,
    trim(city)                                     as city,
    trim(state)                                    as state,
    trim(zip)                                      as zip,
    trim(country)                                  as country,
    (termination_date is null or trim(termination_date) = '' or
     try_to_date(termination_date, 'YYYY-MM-DD') > current_date()) as is_currently_excluded,
    (trim(entity_name) is not null and trim(last_name) is null) as is_entity_not_individual,
    _loaded_at
from base
qualify row_number() over (
    partition by coalesce(nullif(trim(uei), ''), entity_name || activation_date)
    order by _loaded_at desc
) = 1
