{{ config(materialized='view') }}

-- GRAIN: one row per storage generator (plant_code + generator_id) -- verified exact-unique
-- (786 rows) against the 2024-vintage landing table. EIA-860 Schedule 3.4: energy storage
-- detail (batteries etc.): energy capacity, charge/discharge rates, use cases, coupling.
-- NOTE: STORAGE_TECHNOLOGY_3/4 land as NUMBER (all-null columns type-inferred); cast to text.
-- Upgraded 2026-08-10 from auto-generated minimal passthrough (wave 4).

with source as (

    select * from {{ source('ripple_raw', 'FED_EIA860_3_4_ENERGY_STORAGE') }}

),

renamed as (

    select

        -- identifiers
        try_to_number(trim(PLANT_CODE))                        as plant_code,
        trim(GENERATOR_ID)                                     as generator_id,
        try_to_number(trim(UTILITY_ID))                        as utility_id,

        -- dimensions
        trim(UTILITY_NAME)                                     as utility_name,
        trim(PLANT_NAME)                                       as plant_name,
        trim(STATE)                                            as state,
        trim(COUNTY)                                           as county,
        trim(STATUS)                                           as status,
        trim(TECHNOLOGY)                                       as technology,
        trim(PRIME_MOVER)                                      as prime_mover,
        trim(SECTOR_NAME)                                      as sector_name,
        trim(SECTOR)                                           as sector,
        trim(STORAGE_TECHNOLOGY_1)                             as storage_technology_1,
        trim(STORAGE_TECHNOLOGY_2)                             as storage_technology_2,
        STORAGE_TECHNOLOGY_3::varchar                          as storage_technology_3,
        STORAGE_TECHNOLOGY_4::varchar                          as storage_technology_4,
        trim(STORAGE_ENCLOSURE_TYPE)                           as storage_enclosure_type,
        trim(ARBITRAGE)                                        as arbitrage,
        trim(FREQUENCY_REGULATION)                             as frequency_regulation,
        trim(LOAD_FOLLOWING)                                   as load_following,
        trim(RAMPING_SPINNING_RESERVE)                         as ramping_spinning_reserve,
        trim(CO_LOCATED_RENEWABLE_FIRMING)                     as co_located_renewable_firming,
        trim(TRANSMISSION_AND_DISTRIBUTION_DEFERRAL)           as transmission_and_distribution_deferral,
        trim(SYSTEM_PEAK_SHAVING)                              as system_peak_shaving,
        trim(LOAD_MANAGEMENT)                                  as load_management,
        trim(VOLTAGE_OR_REACTIVE_POWER_SUPPORT)                as voltage_or_reactive_power_support,
        trim(BACKUP_POWER)                                     as backup_power,
        trim(EXCESS_WIND_AND_SOLAR_GENERATION)                 as excess_wind_and_solar_generation,
        trim(AC_COUPLED)                                       as ac_coupled,
        trim(DC_COUPLED)                                       as dc_coupled,
        trim(DC_TIGHTLY_COUPLED)                               as dc_tightly_coupled,
        trim(INDEPENDENT)                                      as independent,
        trim(DIRECT_SUPPORT_OF_ANOTHER_UNIT)                   as direct_support_of_another_unit,
        try_to_number(trim(DIRECT_SUPPORT_PLANT_ID_1))         as direct_support_plant_id_1,
        trim(DIRECT_SUPPORT_GEN_ID_1)                          as direct_support_gen_id_1,
        try_to_number(trim(DIRECT_SUPPORT_PLANT_ID_2))         as direct_support_plant_id_2,
        trim(DIRECT_SUPPORT_GEN_ID_2)                          as direct_support_gen_id_2,
        try_to_number(trim(DIRECT_SUPPORT_PLANT_ID_3))         as direct_support_plant_id_3,
        trim(DIRECT_SUPPORT_GEN_ID_3)                          as direct_support_gen_id_3,
        trim(SUPPORT_T_D_ASSET)                                as support_t_d_asset,

        -- measures
        try_to_number(trim(NAMEPLATE_CAPACITY_MW))             as nameplate_capacity_mw,
        try_to_number(trim(SUMMER_CAPACITY_MW))                as summer_capacity_mw,
        try_to_number(trim(WINTER_CAPACITY_MW))                as winter_capacity_mw,
        try_to_number(trim(OPERATING_MONTH))                   as operating_month,
        try_to_number(trim(OPERATING_YEAR))                    as operating_year,
        try_to_number(trim(NAMEPLATE_ENERGY_CAPACITY_MWH))     as nameplate_energy_capacity_mwh,
        try_to_number(trim(MAXIMUM_CHARGE_RATE_MW))            as maximum_charge_rate_mw,
        try_to_number(trim(MAXIMUM_DISCHARGE_RATE_MW))         as maximum_discharge_rate_mw,
        try_to_number(trim(NAMEPLATE_REACTIVE_POWER_RATING))   as nameplate_reactive_power_rating,

        -- metadata
        try_to_timestamp(_INGESTED_AT)                         as _loaded_at,
        _SOURCE_RUN_ID                                         as _source_run_id,
        _SRC_FILE                                              as _src_file

    from source

)

select * from renamed
where plant_code is not null
  and generator_id is not null
