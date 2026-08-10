{{ config(materialized='view') }}

-- GRAIN: one row per boiler (plant_code + boiler_id) -- verified exact-unique
-- (4,429 rows) against the 2024-vintage landing table. EIA-860 Schedule 6.2:
-- boiler-level emissions regulation and control-equipment detail.
-- Upgraded 2026-08-10 from auto-generated minimal passthrough (wave 4).

with source as (

    select * from {{ source('ripple_raw', 'FED_EIA860_6_2_ENVIROEQUIP') }}

),

renamed as (

    select

        -- identifiers
        try_to_number(trim(PLANT_CODE))                       as plant_code,
        trim(BOILER_ID)                                       as boiler_id,
        try_to_number(trim(UTILITY_ID))                       as utility_id,

        -- dimensions
        trim(UTILITY_NAME)                                    as utility_name,
        trim(PLANT_NAME)                                      as plant_name,
        trim(STATE)                                           as state,
        trim(BOILER_STATUS)                                   as boiler_status,
        trim(TYPE_OF_BOILER)                                  as type_of_boiler,
        trim(NEW_SOURCE_REVIEW)                               as new_source_review,
        trim(NEW_SOURCE_REVIEW_PERMIT)                        as new_source_review_permit,
        trim(REGULATION_SULFUR)                               as regulation_sulfur,
        trim(UNIT_SULFUR)                                     as unit_sulfur,
        trim(PERIOD_SULFUR)                                   as period_sulfur,
        trim(SULFUR_DIOXIDE_CONTROL_EXISTING_STRATEGY_1)      as sulfur_dioxide_control_existing_strategy_1,
        trim(SULFUR_DIOXIDE_CONTROL_EXISTING_STRATEGY_2)      as sulfur_dioxide_control_existing_strategy_2,
        trim(SULFUR_DIOXIDE_CONTROL_EXISTING_STRATEGY_3)      as sulfur_dioxide_control_existing_strategy_3,
        trim(SULFUR_DIOXIDE_CONTROL_PROPOSED_STRATEGY_1)      as sulfur_dioxide_control_proposed_strategy_1,
        trim(SULFUR_DIOXIDE_CONTROL_PROPOSED_STRATEGY_2)      as sulfur_dioxide_control_proposed_strategy_2,
        trim(SULFUR_DIOXIDE_CONTROL_PROPOSED_STRATEGY_3)      as sulfur_dioxide_control_proposed_strategy_3,
        trim(REGULATION_NITROGEN)                             as regulation_nitrogen,
        trim(UNIT_NITROGEN)                                   as unit_nitrogen,
        trim(PERIOD_NITROGEN)                                 as period_nitrogen,
        trim(NITROGEN_OXIDE_CONTROL_EXISTING_STRATEGY_1)      as nitrogen_oxide_control_existing_strategy_1,
        trim(NITROGEN_OXIDE_CONTROL_EXISTING_STRATEGY_2)      as nitrogen_oxide_control_existing_strategy_2,
        trim(NITROGEN_OXIDE_CONTROL_EXISTING_STRATEGY_3)      as nitrogen_oxide_control_existing_strategy_3,
        trim(NITROGEN_OXIDE_CONTROL_PROPOSED_STRATEGY_1)      as nitrogen_oxide_control_proposed_strategy_1,
        trim(NITROGEN_OXIDE_CONTROL_PROPOSED_STRATEGY_2)      as nitrogen_oxide_control_proposed_strategy_2,
        trim(NITROGEN_OXIDE_CONTROL_PROPOSED_STRATEGY_3)      as nitrogen_oxide_control_proposed_strategy_3,
        trim(REGULATION_PARTICULATE)                          as regulation_particulate,
        trim(UNIT_PARTICULATE)                                as unit_particulate,
        trim(PERIOD_PARTICULATE)                              as period_particulate,
        trim(REGULATION_MERCURY)                              as regulation_mercury,
        trim(MERCURY_CONTROL_EXISTING_STRATEGY_1)             as mercury_control_existing_strategy_1,
        trim(MERCURY_CONTROL_EXISTING_STRATEGY_2)             as mercury_control_existing_strategy_2,
        trim(MERCURY_CONTROL_EXISTING_STRATEGY_3)             as mercury_control_existing_strategy_3,
        trim(MERCURY_CONTROL_PROPOSED_STRATEGY_1)             as mercury_control_proposed_strategy_1,
        trim(MERCURY_CONTROL_PROPOSED_STRATEGY_2)             as mercury_control_proposed_strategy_2,
        trim(MERCURY_CONTROL_PROPOSED_STRATEGY_3)             as mercury_control_proposed_strategy_3,
        try_to_number(trim(STEAM_PLANT_TYPE))                 as steam_plant_type,

        -- measures
        try_to_number(trim(NEW_SOURCE_REVIEW_MONTH))          as new_source_review_month,
        try_to_number(trim(NEW_SOURCE_REVIEW_YEAR))           as new_source_review_year,
        try_to_number(trim(STANDARD_SULFUR_RATE))             as standard_sulfur_rate,
        try_to_number(trim(STANDARD_SULFUR_PERCENT_SCRUBBED)) as standard_sulfur_percent_scrubbed,
        try_to_number(trim(COMPLIANCE_YEAR_SULFUR))           as compliance_year_sulfur,
        try_to_number(trim(STANDARD_NITROGEN_RATE))           as standard_nitrogen_rate,
        try_to_number(trim(COMPLIANCE_YEAR_NITROGEN))         as compliance_year_nitrogen,
        try_to_number(trim(STANDARD_PARTICULATE_RATE))        as standard_particulate_rate,
        try_to_number(trim(COMPLIANCE_YEAR_PARTICULATE))      as compliance_year_particulate,
        try_to_number(trim(COMPLIANCE_YEAR_MERCURY))          as compliance_year_mercury,

        -- metadata
        try_to_timestamp(_INGESTED_AT)                        as _loaded_at,
        _SOURCE_RUN_ID                                        as _source_run_id,
        _SRC_FILE                                             as _src_file

    from source

)

select * from renamed
where plant_code is not null
  and boiler_id is not null
