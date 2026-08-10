{{ config(materialized='view') }}

-- GRAIN: one row per multifuel generator (plant_code + generator_id) -- verified
-- exact-unique (2,893 rows) against the 2024-vintage landing table. EIA-860
-- Schedule 3.5: fuel-switching capability detail for multi-fuel generators.
-- Upgraded 2026-08-10 from auto-generated minimal passthrough (wave 4).

with source as (

    select * from {{ source('ripple_raw', 'FED_EIA860_3_5_MULTIFUEL') }}

),

renamed as (

    select

        -- identifiers
        try_to_number(trim(PLANT_CODE))                              as plant_code,
        trim(GENERATOR_ID)                                           as generator_id,
        try_to_number(trim(UTILITY_ID))                              as utility_id,

        -- dimensions
        trim(UTILITY_NAME)                                           as utility_name,
        trim(PLANT_NAME)                                             as plant_name,
        trim(STATE)                                                  as state,
        trim(COUNTY)                                                 as county,
        trim(STATUS)                                                 as status,
        trim(TECHNOLOGY)                                             as technology,
        trim(PRIME_MOVER)                                            as prime_mover,
        trim(SECTOR_NAME)                                            as sector_name,
        trim(SECTOR)                                                 as sector,
        trim(ENERGY_SOURCE_1)                                        as energy_source_1,
        trim(ENERGY_SOURCE_2)                                        as energy_source_2,
        trim(MULTIPLE_FUELS)                                         as multiple_fuels,
        trim(COFIRE_FUELS)                                           as cofire_fuels,
        trim(COFIRE_ENERGY_SOURCE_1)                                 as cofire_energy_source_1,
        trim(COFIRE_ENERGY_SOURCE_2)                                 as cofire_energy_source_2,
        trim(COFIRE_ENERGY_SOURCE_3)                                 as cofire_energy_source_3,
        trim(COFIRE_ENERGY_SOURCE_4)                                 as cofire_energy_source_4,
        trim(COFIRE_ENERGY_SOURCE_5)                                 as cofire_energy_source_5,
        trim(COFIRE_ENERGY_SOURCE_6)                                 as cofire_energy_source_6,
        trim(SWITCH_BETWEEN_OIL_AND_NATURAL_GAS)                     as switch_between_oil_and_natural_gas,
        trim(SWITCH_WHEN_OPERATING)                                  as switch_when_operating,
        trim(TIME_TO_SWITCH_FROM_GAS_TO_OIL)                         as time_to_switch_from_gas_to_oil,
        trim(TIME_TO_SWITCH_FROM_OIL_TO_GAS)                         as time_to_switch_from_oil_to_gas,
        trim(FACTORS_THAT_LIMIT_SWITCHING)                           as factors_that_limit_switching,
        trim(STORAGE_LIMITS)                                         as storage_limits,
        trim(AIR_PERMIT_LIMITS)                                      as air_permit_limits,
        trim(OTHER_LIMITS)                                           as other_limits,

        -- measures
        try_to_number(trim(NAMEPLATE_CAPACITY_MW))                   as nameplate_capacity_mw,
        try_to_number(trim(SUMMER_CAPACITY_MW))                      as summer_capacity_mw,
        try_to_number(trim(WINTER_CAPACITY_MW))                      as winter_capacity_mw,
        try_to_number(trim(OPERATING_MONTH))                         as operating_month,
        try_to_number(trim(OPERATING_YEAR))                          as operating_year,
        try_to_number(trim(NET_SUMMER_CAPACITY_WITH_NATURAL_GAS_MW)) as net_summer_capacity_with_natural_gas_mw,
        try_to_number(trim(NET_WINTER_CAPACITY_WITH_NATURAL_GAS_MW)) as net_winter_capacity_with_natural_gas_mw,
        try_to_number(trim(NET_SUMMER_CAPACITY_WITH_OIL_MW))         as net_summer_capacity_with_oil_mw,
        try_to_number(trim(NET_WINTER_CAPACITY_WITH_OIL_MW))         as net_winter_capacity_with_oil_mw,

        -- metadata
        try_to_timestamp(_INGESTED_AT)                               as _loaded_at,
        _SOURCE_RUN_ID                                               as _source_run_id,
        _SRC_FILE                                                    as _src_file

    from source

)

select * from renamed
where plant_code is not null
  and generator_id is not null
