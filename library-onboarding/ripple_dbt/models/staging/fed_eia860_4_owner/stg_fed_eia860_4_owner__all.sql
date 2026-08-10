{{ config(materialized='view') }}

-- GRAIN: one row per generator-owner stake (plant_code + generator_id + ownership_id)
-- -- verified exact-unique (5,496 rows) against the 2024-vintage landing table.
-- EIA-860 Schedule 4: fractional ownership of jointly-owned generators.
-- Upgraded 2026-08-10 from auto-generated minimal passthrough (wave 4).

with source as (

    select * from {{ source('ripple_raw', 'FED_EIA860_4_OWNER') }}

),

renamed as (

    select

        -- identifiers
        try_to_number(trim(PLANT_CODE))            as plant_code,
        trim(GENERATOR_ID)                         as generator_id,
        try_to_number(trim(OWNERSHIP_ID))          as ownership_id,
        try_to_number(trim(UTILITY_ID))            as utility_id,

        -- dimensions
        trim(UTILITY_NAME)                         as utility_name,
        trim(PLANT_NAME)                           as plant_name,
        trim(STATE)                                as state,
        trim(STATUS)                               as status,
        trim(OWNER_NAME)                           as owner_name,
        trim(OWNER_STREET_ADDRESS)                 as owner_street_address,
        trim(OWNER_CITY)                           as owner_city,
        trim(OWNER_STATE)                          as owner_state,
        trim(OWNER_ZIP)                            as owner_zip,

        -- measures
        try_to_number(trim(PERCENT_OWNED))         as percent_owned,

        -- metadata
        try_to_timestamp(_INGESTED_AT)             as _loaded_at,
        _SOURCE_RUN_ID                             as _source_run_id,
        _SRC_FILE                                  as _src_file

    from source

)

select * from renamed
where plant_code is not null
  and generator_id is not null
  and ownership_id is not null
