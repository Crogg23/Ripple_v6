{{ config(materialized='view') }}

-- GRAIN: one row per utility (utility_id) -- verified exact-unique (6,643 rows) against the
-- 2024-vintage landing table. EIA-860 Schedule 1: utilities that own/operate/manage plants.
-- Upgraded 2026-08-10 from auto-generated minimal passthrough (wave 4).

with source as (

    select * from {{ source('ripple_raw', 'FED_EIA860_1_UTILITY') }}

),

renamed as (

    select

        -- identifiers
        try_to_number(trim(UTILITY_ID))                          as utility_id,

        -- dimensions
        trim(UTILITY_NAME)                                       as utility_name,
        trim(STREET_ADDRESS)                                     as street_address,
        trim(CITY)                                               as city,
        trim(STATE)                                              as state,
        trim(ZIP)                                                as zip,
        trim(OWNER_OF_PLANTS_REPORTED_ON_FORM)                   as owner_of_plants_reported_on_form,
        trim(OPERATOR_OF_PLANTS_REPORTED_ON_FORM)                as operator_of_plants_reported_on_form,
        trim(ASSET_MANAGER_OF_PLANTS_REPORTED_ON_FORM)           as asset_manager_of_plants_reported_on_form,
        trim(OTHER_RELATIONSHIPS_WITH_PLANTS_REPORTED_ON_FORM)   as other_relationships_with_plants_reported_on_form,
        trim(ENTITY_TYPE)                                        as entity_type,

        -- metadata
        try_to_timestamp(_INGESTED_AT)                           as _loaded_at,
        _SOURCE_RUN_ID                                           as _source_run_id,
        _SRC_FILE                                                as _src_file

    from source

)

select * from renamed
where utility_id is not null
