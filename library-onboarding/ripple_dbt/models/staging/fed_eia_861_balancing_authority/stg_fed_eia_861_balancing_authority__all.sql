{{ config(materialized='view') }}

-- GRAIN: one row per balancing authority x state (ba_id + state) -- verified exact-unique
-- (189 rows) against the 2024-vintage landing table. EIA-861 Balancing Authority sheet:
-- which balancing authorities operate in which states.
-- NOTE: reads FED_EIA_861_BALANCING_AUTHORITY (underscore after EIA), the clean re-ingest
-- with real headers. The header-corrupted twin FED_EIA861_BALANCING_AUTHORITY is being
-- dropped -- do not model it. Metadata cols here have NO leading underscore and
-- INGESTED_AT is a NUMBER epoch.
-- Authored 2026-08-10 (wave 4).

with source as (

    select * from {{ source('ripple_raw', 'FED_EIA_861_BALANCING_AUTHORITY') }}

),

renamed as (

    select

        -- identifiers
        try_to_number(trim(BA_ID))                 as ba_id,
        trim(STATE)                                as state,

        -- dimensions
        try_to_number(trim(DATA_YEAR))             as data_year,
        trim(BA_CODE)                              as ba_code,
        trim(BALANCING_AUTHORITY_NAME)             as balancing_authority_name,

        -- metadata
        -- FIXED 2026-08-20 (time-index scan): INGESTED_AT is MICROSECONDS since epoch
        -- (e.g. 1785965270036203). A bare to_timestamp reads it as SECONDS and
        -- lands the row in the year 56,596,956 -- which is what poisoned this
        -- table's measured date range. The `, 6` scale argument is the fix.
        to_timestamp_ntz(INGESTED_AT, 6)                  as _loaded_at,
        SOURCE_RUN_ID                              as _source_run_id,
        SRC_SHA256                                 as _src_sha256

    from source

)

select * from renamed
where ba_id is not null
  and state is not null
