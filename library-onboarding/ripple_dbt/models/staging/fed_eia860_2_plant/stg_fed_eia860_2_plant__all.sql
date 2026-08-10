{{ config(materialized='view') }}

-- GRAIN: one row per plant (plant_code) -- verified exact-unique (16,132 rows) against the
-- 2024-vintage landing table. EIA-860 Schedule 2: plant-level location/grid attributes.
-- Upgraded 2026-08-10 from auto-generated minimal passthrough (wave 4).

with source as (

    select * from {{ source('ripple_raw', 'FED_EIA860_2_PLANT') }}

),

renamed as (

    select

        -- identifiers
        try_to_number(trim(PLANT_CODE))                              as plant_code,
        try_to_number(trim(UTILITY_ID))                              as utility_id,

        -- dimensions
        trim(UTILITY_NAME)                                           as utility_name,
        trim(PLANT_NAME)                                             as plant_name,
        trim(STREET_ADDRESS)                                         as street_address,
        trim(CITY)                                                   as city,
        trim(STATE)                                                  as state,
        trim(ZIP)                                                    as zip,
        trim(COUNTY)                                                 as county,
        try_to_number(trim(LATITUDE))                                as latitude,
        try_to_number(trim(LONGITUDE))                               as longitude,
        trim(NERC_REGION)                                            as nerc_region,
        trim(BALANCING_AUTHORITY_CODE)                               as balancing_authority_code,
        trim(BALANCING_AUTHORITY_NAME)                               as balancing_authority_name,
        trim(NAME_OF_WATER_SOURCE)                                   as name_of_water_source,
        trim(PRIMARY_PURPOSE_NAICS_CODE)                             as primary_purpose_naics_code,
        trim(REGULATORY_STATUS)                                      as regulatory_status,
        trim(SECTOR)                                                 as sector,
        trim(SECTOR_NAME)                                            as sector_name,
        trim(FERC_COGENERATION_STATUS)                               as ferc_cogeneration_status,
        trim(FERC_COGENERATION_DOCKET_NUMBER)                        as ferc_cogeneration_docket_number,
        trim(FERC_SMALL_POWER_PRODUCER_STATUS)                       as ferc_small_power_producer_status,
        trim(FERC_SMALL_POWER_PRODUCER_DOCKET_NUMBER)                as ferc_small_power_producer_docket_number,
        trim(FERC_EXEMPT_WHOLESALE_GENERATOR_STATUS)                 as ferc_exempt_wholesale_generator_status,
        trim(FERC_EXEMPT_WHOLESALE_GENERATOR_DOCKET_NUMBER)          as ferc_exempt_wholesale_generator_docket_number,
        trim(ASH_IMPOUNDMENT)                                        as ash_impoundment,
        trim(ASH_IMPOUNDMENT_LINED)                                  as ash_impoundment_lined,
        trim(ASH_IMPOUNDMENT_STATUS)                                 as ash_impoundment_status,
        trim(TRANSMISSION_OR_DISTRIBUTION_SYSTEM_OWNER)              as transmission_or_distribution_system_owner,
        try_to_number(trim(TRANSMISSION_OR_DISTRIBUTION_SYSTEM_OWNER_ID))
                                                                     as transmission_or_distribution_system_owner_id,
        trim(TRANSMISSION_OR_DISTRIBUTION_SYSTEM_OWNER_STATE)        as transmission_or_distribution_system_owner_state,
        try_to_number(trim(GRID_VOLTAGE_KV))                         as grid_voltage_kv,
        try_to_number(trim(GRID_VOLTAGE_2_KV))                       as grid_voltage_2_kv,
        try_to_number(trim(GRID_VOLTAGE_3_KV))                       as grid_voltage_3_kv,
        trim(ENERGY_STORAGE)                                         as energy_storage,
        trim(NATURAL_GAS_LDC_NAME)                                   as natural_gas_ldc_name,
        trim(NATURAL_GAS_PIPELINE_NAME_1)                            as natural_gas_pipeline_name_1,
        trim(NATURAL_GAS_PIPELINE_NAME_2)                            as natural_gas_pipeline_name_2,
        trim(NATURAL_GAS_PIPELINE_NAME_3)                            as natural_gas_pipeline_name_3,
        trim(PIPELINE_NOTES)                                         as pipeline_notes,
        trim(NATURAL_GAS_STORAGE)                                    as natural_gas_storage,
        trim(LIQUEFIED_NATURAL_GAS_STORAGE)                          as liquefied_natural_gas_storage,

        -- metadata
        try_to_timestamp(_INGESTED_AT)                               as _loaded_at,
        _SOURCE_RUN_ID                                               as _source_run_id,
        _SRC_FILE                                                    as _src_file

    from source

)

select * from renamed
where plant_code is not null
