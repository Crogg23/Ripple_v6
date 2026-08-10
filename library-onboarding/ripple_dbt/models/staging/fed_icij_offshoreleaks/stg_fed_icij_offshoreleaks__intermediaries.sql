{{ config(materialized='view') }}

/*
  Hand-built 2026-08-09 (73-source backlog). ICIJ Offshore Leaks
  intermediaries: the law firms/banks/agents that set up offshore entities.
  Grain: one row = one intermediary node; node_id verified unique
  (26,768 = 26,768).
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_ICIJ_OFFSHORELEAKS_INTERMEDIARIES') }}
),

renamed as (
    select
        nullif(trim(NODE_ID), '')                                 as node_id,
        nullif(trim(NAME), '')                                    as name,
        nullif(trim(STATUS), '')                                  as status,
        nullif(trim(INTERNAL_ID), '')                             as internal_id,
        nullif(trim(ADDRESS), '')                                 as address,
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
