{{ config(materialized='view') }}

/*
  Hand-built 2026-08-09 (73-source backlog, wave 2). Missouri State Highway
  Patrol public sex offender registry export.
  Grain: one row = one registrant-offense (a person with multiple qualifying
  offenses appears once per offense; 28,185 rows / 21,254 distinct names).
  No unique key exists in the export -- no unique test.
  DATE_OF_BIRTH is an ISO timestamp string.
*/

with source as (
    select * from {{ source('ripple_raw', 'STATE_MO_SEX_OFFENDER_REGISTRY') }}
),

renamed as (
    select
        nullif(trim(NAME), '')                          as registrant_name,
        nullif(trim(ADDRESS), '')                       as address,
        nullif(trim(CITY), '')                          as city,
        nullif(trim(ST), '')                            as state,
        nullif(trim(ZIP), '')                           as zip,
        nullif(trim(COUNTY), '')                        as county,
        nullif(trim(OFFENSE), '')                       as offense,
        try_to_number("COUNT")                          as offense_count,
        (upper(trim(COMPLIANT)) = 'Y')                  as is_compliant,
        nullif(trim(TIER), '')                          as tier,
        try_to_date(nullif(trim(DATE_OF_BIRTH), ''))    as date_of_birth,
        to_timestamp_ntz(INGESTED_AT, 6)                as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                 as _source_run_id
    from source
)

select * from renamed
