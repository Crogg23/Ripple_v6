{{ config(materialized='view') }}

/*
  Hand-built 2026-08-09 (73-source backlog). OpenSanctions default collection
  (simplified targets CSV): every person, company, vessel, aircraft, crypto
  wallet etc. currently targeted by a sanctions list, PEP list or enforcement
  dataset worldwide, consolidated and deduplicated by OpenSanctions.
  Grain: one row = one target; id verified unique (1,281,846 = 1,281,846).
  Multi-valued fields (aliases, countries, addresses, identifiers, sanctions,
  datasets) are semicolon-delimited strings as published.
*/

with source as (
    select * from {{ source('ripple_raw', 'INTL_OPENSANCTIONS_DEFAULT') }}
),

renamed as (
    select
        nullif(trim(ID), '')                                      as id,
        nullif(trim(C_SCHEMA), '')                                as entity_type,
        nullif(trim(NAME), '')                                    as name,
        nullif(trim(ALIASES), '')                                 as aliases,
        nullif(trim(BIRTH_DATE), '')                              as birth_date,
        nullif(trim(COUNTRIES), '')                               as countries,
        nullif(trim(ADDRESSES), '')                               as addresses,
        nullif(trim(IDENTIFIERS), '')                             as identifiers,
        nullif(trim(SANCTIONS), '')                               as sanctions,
        nullif(trim(PHONES), '')                                  as phones,
        nullif(trim(EMAILS), '')                                  as emails,
        nullif(trim(PROGRAM_IDS), '')                             as program_ids,
        nullif(trim(DATASET), '')                                 as datasets,
        try_to_timestamp_ntz(trim(FIRST_SEEN))                    as first_seen,
        try_to_timestamp_ntz(trim(LAST_SEEN))                     as last_seen,
        try_to_timestamp_ntz(trim(LAST_CHANGE))                   as last_change,
        to_timestamp_ntz(_INGESTED_AT)                            as _ingested_at,
        nullif(trim(_SOURCE_RUN_ID), '')                          as _source_run_id
    from source
)

select * from renamed
