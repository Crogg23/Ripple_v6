{{ config(materialized='view') }}

/*
  Generated 2026-08-09 (73-source backlog, wave 2d).
  SAMPLE ONLY -- NOT the full dataset. DHS HIFLD infrastructure facilities: a 500-row slice of one layer. objectid+layer unique in the slice. Use for shape/testing only.
  Grain: one row = one facility in the sampled layer.
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_DHS_HIFLD') }}
),

renamed as (
    select
        nullif(trim(OBJECTID), '')                                 as objectid,
        nullif(trim(NAME), '')                                     as name,
        nullif(trim(ADDRESS), '')                                  as address,
        nullif(trim(CITY), '')                                     as city,
        nullif(trim(STATE), '')                                    as state,
        nullif(trim(ZIP), '')                                      as zip,
        nullif(trim(COUNTY), '')                                   as county,
        nullif(trim(FIPS), '')                                     as fips,
        try_to_number(nullif(trim(LATITUDE), ''), 18, 4)           as latitude,
        try_to_number(nullif(trim(LONGITUDE), ''), 18, 4)          as longitude,
        nullif(trim(NAICS_CODE), '')                               as naics_code,
        nullif(trim(LAYER_NAME), '')                               as layer_name,
        nullif(trim(STATUS), '')                                   as status,
        nullif(trim(OWNER), '')                                    as owner,
        try_to_date(left(nullif(trim(SOURCE_DATE), ''), 10))       as source_date,
        to_timestamp_ntz(_INGESTED_AT, 6)                          as _ingested_at,
        nullif(trim(_SOURCE_RUN_ID), '')                           as _source_run_id
    from source
)

select * from renamed
