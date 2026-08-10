{{ config(materialized='view') }}

/*
  Hand-built 2026-08-09 (73-source backlog). ICIJ Offshore Leaks officers:
  people and companies acting as directors/shareholders/beneficiaries of
  offshore entities. Grain: one row = one officer node; node_id verified
  unique (771,315 = 771,315).
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_ICIJ_OFFSHORELEAKS_OFFICERS') }}
),

renamed as (
    select
        nullif(trim(NODE_ID), '')                                 as node_id,
        nullif(trim(NAME), '')                                    as name,
        nullif(trim(COUNTRIES), '')                               as countries,
        nullif(trim(COUNTRY_CODES), '')                           as country_codes,
        nullif(trim(SOURCEID), '')                                as source_leak,
        nullif(trim(VALID_UNTIL), '')                             as valid_until,
        nullif(trim(NOTE), '')                                    as note,
        to_timestamp_ntz(INGESTED_AT)                             as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                           as _source_run_id
    from source
)

select * from renamed
