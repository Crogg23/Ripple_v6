{{ config(materialized='view') }}

-- Built 2026-08-10 (backlog wave 3). EPA RCRAInfo hazardous-waste handler universe: one row = one RCRA handler (ID_NUMBER unique). Name, address, enforcement universe flags, generator status.

with

source as (

    select * from {{ source('ripple_raw', 'FED_EPA_RCRA_FACILITIES') }}

),

renamed as (

    select

        {{ dbt_utils.generate_surrogate_key(['id_number']) }}
                                                        as handler_id,

        trim(ID_NUMBER)                                         as id_number,
        trim(FACILITY_NAME)                                     as facility_name,
        trim(ACTIVITY_LOCATION)                                 as activity_location,
        trim(FULL_ENFORCEMENT)                                  as full_enforcement,
        trim(HREPORT_UNIVERSE_RECORD)                           as hreport_universe_record,
        trim(STREET_ADDRESS)                                    as street_address,
        trim(CITY_NAME)                                         as city_name,
        trim(STATE_CODE)                                        as state_code,
        trim(ZIP_CODE)                                          as zip_code,
        try_to_number(trim(LATITUDE83))                         as latitude83,
        try_to_number(trim(LONGITUDE83))                        as longitude83,
        trim(FED_WASTE_GENERATOR)                               as fed_waste_generator,

        -- metadata
        ingested_at as _ingested_at,
        source_run_id as _source_run_id

    from source

)

select * from renamed
