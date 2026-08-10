{{ config(materialized='view') }}

/*
  Rewritten 2026-08-09: the rebuild replaced the old incident-level landing
  shape (the estimate API it came from is retired) with state x offense x month
  x series counts from the live summarized CDE endpoints, back to 1985.
  SERIES distinguishes reported OFFENSES from CLEARANCES.
  (state, offense, month, series) verified unique (477,360 = 477,360).
  MONTH lands as 'MM-YYYY' — month_date casts it (day defaults to the 1st).
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_FBI_CDE') }}
),

renamed as (
    select
        nullif(trim(STATE), '')                                           as state,
        nullif(trim(OFFENSE), '')                                         as offense,
        nullif(trim(SERIES), '')                                          as series,
        nullif(trim(MONTH), '')                                           as month,
        try_to_date(trim(MONTH), 'MM-YYYY')                               as month_date,
        try_to_number(replace(trim(COUNT), ',', ''))                      as count,
        try_to_double(replace(trim(RATE_PER_100K), ',', ''))              as rate_per_100k,
        to_timestamp_ntz(_INGESTED_AT, 6)                                 as _ingested_at,
        nullif(trim(_SOURCE_RUN_ID), '')                                  as _source_run_id
    from source
)

select * from renamed
