{{ config(materialized='view') }}

-- GRAIN: one row per generator (plant_code + generator_id) -- verified exact-unique
-- (26,856 rows) against the 2024-vintage landing table. EIA-860 Schedule 3.1: every
-- operable/proposed generator with capacity, status, fuel, and planned-change detail.
-- Upgraded 2026-08-10 from auto-generated minimal passthrough (wave 4).

with source as (

    select * from {{ source('ripple_raw', 'FED_EIA860_3_1_GENERATOR') }}

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
        trim(TECHNOLOGY)                                             as technology,
        trim(PRIME_MOVER)                                            as prime_mover,
        trim(UNIT_CODE)                                              as unit_code,
        trim(OWNERSHIP)                                              as ownership,
        trim(DUCT_BURNERS)                                           as duct_burners,
        trim(CAN_BYPASS_HEAT_RECOVERY_STEAM_GENERATOR)               as can_bypass_heat_recovery_steam_generator,
        trim(RTO_ISO_LMP_NODE_DESIGNATION)                           as rto_iso_lmp_node_designation,
        trim(RTO_ISO_LOCATION_DESIGNATION_FOR_REPORTING_WHOLESALE_SALES_DATA_TO_FERC)
                                                                     as rto_iso_location_designation_for_reporting_wholesale_sales_data_to_ferc,
        trim(STATUS)                                                 as status,
        trim(SYNCHRONIZED_TO_TRANSMISSION_GRID)                      as synchronized_to_transmission_grid,
        trim(ASSOCIATED_WITH_COMBINED_HEAT_AND_POWER_SYSTEM)         as associated_with_combined_heat_and_power_system,
        trim(SECTOR_NAME)                                            as sector_name,
        trim(SECTOR)                                                 as sector,
        trim(TOPPING_OR_BOTTOMING)                                   as topping_or_bottoming,
        trim(ENERGY_SOURCE_1)                                        as energy_source_1,
        trim(ENERGY_SOURCE_2)                                        as energy_source_2,
        trim(ENERGY_SOURCE_3)                                        as energy_source_3,
        trim(ENERGY_SOURCE_4)                                        as energy_source_4,
        trim(ENERGY_SOURCE_5)                                        as energy_source_5,
        trim(ENERGY_SOURCE_6)                                        as energy_source_6,
        trim(STARTUP_SOURCE_1)                                       as startup_source_1,
        trim(STARTUP_SOURCE_2)                                       as startup_source_2,
        trim(STARTUP_SOURCE_3)                                       as startup_source_3,
        trim(STARTUP_SOURCE_4)                                       as startup_source_4,
        trim(SOLID_FUEL_GASIFICATION_SYSTEM)                         as solid_fuel_gasification_system,
        trim(CARBON_CAPTURE_TECHNOLOGY)                              as carbon_capture_technology,
        trim(TIME_FROM_COLD_SHUTDOWN_TO_FULL_LOAD)                   as time_from_cold_shutdown_to_full_load,
        trim(FLUIDIZED_BED_TECHNOLOGY)                               as fluidized_bed_technology,
        trim(PULVERIZED_COAL_TECHNOLOGY)                             as pulverized_coal_technology,
        trim(STOKER_TECHNOLOGY)                                      as stoker_technology,
        trim(OTHER_COMBUSTION_TECHNOLOGY)                            as other_combustion_technology,
        trim(SUBCRITICAL_TECHNOLOGY)                                 as subcritical_technology,
        trim(SUPERCRITICAL_TECHNOLOGY)                               as supercritical_technology,
        trim(ULTRASUPERCRITICAL_TECHNOLOGY)                          as ultrasupercritical_technology,
        trim(PLANNED_NEW_PRIME_MOVER)                                as planned_new_prime_mover,
        trim(PLANNED_ENERGY_SOURCE_1)                                as planned_energy_source_1,
        trim(OTHER_PLANNED_MODIFICATIONS)                            as other_planned_modifications,
        trim(MULTIPLE_FUELS)                                         as multiple_fuels,
        trim(COFIRE_FUELS)                                           as cofire_fuels,
        trim(SWITCH_BETWEEN_OIL_AND_NATURAL_GAS)                     as switch_between_oil_and_natural_gas,
        trim(UPRATE_OR_DERATE_COMPLETED_DURING_YEAR)                 as uprate_or_derate_completed_during_year,

        -- measures
        try_to_number(trim(NAMEPLATE_CAPACITY_MW))                   as nameplate_capacity_mw,
        try_to_number(trim(NAMEPLATE_POWER_FACTOR))                  as nameplate_power_factor,
        try_to_number(trim(SUMMER_CAPACITY_MW))                      as summer_capacity_mw,
        try_to_number(trim(WINTER_CAPACITY_MW))                      as winter_capacity_mw,
        try_to_number(trim(MINIMUM_LOAD_MW))                         as minimum_load_mw,
        try_to_number(trim(MONTH_UPRATE_OR_DERATE_COMPLETED))        as month_uprate_or_derate_completed,
        try_to_number(trim(YEAR_UPRATE_OR_DERATE_COMPLETED))         as year_uprate_or_derate_completed,
        try_to_number(trim(OPERATING_MONTH))                         as operating_month,
        try_to_number(trim(OPERATING_YEAR))                          as operating_year,
        try_to_number(trim(PLANNED_RETIREMENT_MONTH))                as planned_retirement_month,
        try_to_number(trim(PLANNED_RETIREMENT_YEAR))                 as planned_retirement_year,
        try_to_number(trim(TURBINES_OR_HYDROKINETIC_BUOYS))          as turbines_or_hydrokinetic_buoys,
        try_to_number(trim(PLANNED_NET_SUMMER_CAPACITY_UPRATE_MW))   as planned_net_summer_capacity_uprate_mw,
        try_to_number(trim(PLANNED_NET_WINTER_CAPACITY_UPRATE_MW))   as planned_net_winter_capacity_uprate_mw,
        try_to_number(trim(PLANNED_UPRATE_MONTH))                    as planned_uprate_month,
        try_to_number(trim(PLANNED_UPRATE_YEAR))                     as planned_uprate_year,
        try_to_number(trim(PLANNED_NET_SUMMER_CAPACITY_DERATE_MW))   as planned_net_summer_capacity_derate_mw,
        try_to_number(trim(PLANNED_NET_WINTER_CAPACITY_DERATE_MW))   as planned_net_winter_capacity_derate_mw,
        try_to_number(trim(PLANNED_DERATE_MONTH))                    as planned_derate_month,
        try_to_number(trim(PLANNED_DERATE_YEAR))                     as planned_derate_year,
        try_to_number(trim(PLANNED_NEW_NAMEPLATE_CAPACITY_MW))       as planned_new_nameplate_capacity_mw,
        try_to_number(trim(PLANNED_REPOWER_MONTH))                   as planned_repower_month,
        try_to_number(trim(PLANNED_REPOWER_YEAR))                    as planned_repower_year,
        try_to_number(trim(OTHER_MODIFICATIONS_MONTH))               as other_modifications_month,
        try_to_number(trim(OTHER_MODIFICATIONS_YEAR))                as other_modifications_year,

        -- metadata
        try_to_timestamp(_INGESTED_AT)                               as _loaded_at,
        _SOURCE_RUN_ID                                               as _source_run_id,
        _SRC_FILE                                                    as _src_file

    from source

)

select * from renamed
where plant_code is not null
  and generator_id is not null
