{{ config(materialized='view') }}

-- Built 2026-08-10 (backlog wave 3). EPA RCRAInfo handler NAICS industry codes: one row = one handler-location-NAICS link (exactly unique).

with

source as (

    select * from {{ source('ripple_raw', 'FED_EPA_RCRA_RCRA_NAICS') }}

),

renamed as (

    select

        {{ dbt_utils.generate_surrogate_key(['id_number', 'activity_location', 'naics_code']) }}
                                                        as facility_naics_id,

        trim(ID_NUMBER)                                         as id_number,
        trim(ACTIVITY_LOCATION)                                 as activity_location,
        trim(NAICS_CODE)                                        as naics_code,

        -- metadata
        _ingested_at as _ingested_at,
        _source_run_id as _source_run_id

    from source

)

select * from renamed
