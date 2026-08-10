{{ config(materialized='view') }}

-- GRAIN: one row per wind generator (plant_code + generator_id) -- verified exact-unique
-- (1,563 rows) against the 2024-vintage landing table. EIA-860 Schedule 3.2: wind
-- turbine detail for wind generators.
-- Upgraded 2026-08-10 from auto-generated minimal passthrough (wave 4).

with source as (

    select * from {{ source('ripple_raw', 'FED_EIA860_3_2_WIND') }}

),

renamed as (

    select

        -- identifiers
        try_to_number(trim(PLANT_CODE))                   as plant_code,
        trim(GENERATOR_ID)                                as generator_id,
        try_to_number(trim(UTILITY_ID))                   as utility_id,

        -- dimensions
        trim(UTILITY_NAME)                                as utility_name,
        trim(PLANT_NAME)                                  as plant_name,
        trim(STATE)                                       as state,
        trim(COUNTY)                                      as county,
        trim(STATUS)                                      as status,
        trim(TECHNOLOGY)                                  as technology,
        trim(PRIME_MOVER)                                 as prime_mover,
        trim(SECTOR_NAME)                                 as sector_name,
        trim(SECTOR)                                      as sector,
        trim(PREDOMINANT_TURBINE_MANUFACTURER)            as predominant_turbine_manufacturer,
        trim(PREDOMINANT_TURBINE_MODEL_NUMBER)            as predominant_turbine_model_number,
        trim(WIND_QUALITY_CLASS)                          as wind_quality_class,

        -- measures
        try_to_number(trim(NAMEPLATE_CAPACITY_MW))        as nameplate_capacity_mw,
        try_to_number(trim(SUMMER_CAPACITY_MW))           as summer_capacity_mw,
        try_to_number(trim(WINTER_CAPACITY_MW))           as winter_capacity_mw,
        try_to_number(trim(OPERATING_MONTH))              as operating_month,
        try_to_number(trim(OPERATING_YEAR))               as operating_year,
        try_to_number(trim(NUMBER_OF_TURBINES))           as number_of_turbines,
        try_to_number(trim(DESIGN_WIND_SPEED_MPH))        as design_wind_speed_mph,
        try_to_number(trim(TURBINE_HUB_HEIGHT_FEET))      as turbine_hub_height_feet,

        -- metadata
        try_to_timestamp(_INGESTED_AT)                    as _loaded_at,
        _SOURCE_RUN_ID                                    as _source_run_id,
        _SRC_FILE                                         as _src_file

    from source

)

select * from renamed
where plant_code is not null
  and generator_id is not null
