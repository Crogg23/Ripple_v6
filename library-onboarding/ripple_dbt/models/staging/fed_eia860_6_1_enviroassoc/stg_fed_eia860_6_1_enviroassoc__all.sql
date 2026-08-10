{{ config(materialized='view') }}

-- GRAIN: one row per boiler-generator association (plant_code + boiler_id + generator_id
-- + steam_plant_type) -- verified exact-unique (7,021 rows) against the 2024-vintage
-- landing table. EIA-860 Schedule 6.1: links boilers to the generators they serve.
-- Upgraded 2026-08-10 from auto-generated minimal passthrough (wave 4).

with source as (

    select * from {{ source('ripple_raw', 'FED_EIA860_6_1_ENVIROASSOC') }}

),

renamed as (

    select

        -- identifiers
        try_to_number(trim(PLANT_CODE))        as plant_code,
        trim(BOILER_ID)                        as boiler_id,
        trim(GENERATOR_ID)                     as generator_id,
        try_to_number(trim(STEAM_PLANT_TYPE))  as steam_plant_type,
        try_to_number(trim(UTILITY_ID))        as utility_id,

        -- dimensions
        trim(UTILITY_NAME)                     as utility_name,
        trim(PLANT_NAME)                       as plant_name,

        -- metadata
        try_to_timestamp(_INGESTED_AT)         as _loaded_at,
        _SOURCE_RUN_ID                         as _source_run_id,
        _SRC_FILE                              as _src_file

    from source

)

select * from renamed
where plant_code is not null
