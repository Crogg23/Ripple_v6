{{ config(materialized='view') }}

/*
  Hand-built 2026-08-09 (73-source backlog). ICIJ Offshore Leaks "others":
  miscellaneous nodes (foundations, limited partnerships, etc.) that fit
  neither entity nor officer. Grain: one row = one node; node_id verified
  unique (2,989 = 2,989).
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_ICIJ_OFFSHORELEAKS_OTHERS') }}
),

renamed as (
    select
        nullif(trim(NODE_ID), '')                                 as node_id,
        nullif(trim(NAME), '')                                    as name,
        nullif(trim(TYPE), '')                                    as type,
        try_to_date(trim(INCORPORATION_DATE), 'DD-MON-YYYY')      as incorporation_date,
        try_to_date(trim(STRUCK_OFF_DATE), 'DD-MON-YYYY')         as struck_off_date,
        try_to_date(trim(CLOSED_DATE), 'DD-MON-YYYY')             as closed_date,
        nullif(trim(JURISDICTION), '')                            as jurisdiction,
        nullif(trim(JURISDICTION_DESCRIPTION), '')                as jurisdiction_description,
        nullif(trim(COUNTRIES), '')                               as countries,
        nullif(trim(COUNTRY_CODES), '')                           as country_codes,
        nullif(trim(SOURCEID), '')                                as source_leak,
        nullif(trim(VALID_UNTIL), '')                             as valid_until,
        nullif(trim(NOTE), '')                                    as note,
        -- FIXED 2026-08-20 (time-index scan): INGESTED_AT is MICROSECONDS since epoch
        -- (e.g. 1785965270036203). A bare to_timestamp reads it as SECONDS and
        -- lands the row in the year 56,596,956 -- which is what poisoned this
        -- table's measured date range. The `, 6` scale argument is the fix.
        to_timestamp_ntz(INGESTED_AT, 6)                             as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                           as _source_run_id
    from source
)

select * from renamed
