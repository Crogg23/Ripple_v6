{{ config(materialized='view') }}

-- Built 2026-08-10 (backlog wave 3). EPA RCRAInfo violation / significant-non-compliance monthly history: one row = one handler-location-month status (vio_flag / snc_flag).

with

source as (

    select * from {{ source('ripple_raw', 'FED_EPA_RCRA_VIOSNC_HISTORY') }}

),

renamed as (

    select

        {{ dbt_utils.generate_surrogate_key(['id_number', 'activity_location', 'yrmonth']) }}
                                                        as status_month_id,

        trim(ID_NUMBER)                                         as id_number,
        trim(ACTIVITY_LOCATION)                                 as activity_location,
        trim(YRMONTH)                                           as yrmonth,
        trim(VIO_FLAG)                                          as vio_flag,
        trim(SNC_FLAG)                                          as snc_flag,

        -- metadata
        ingested_at as _ingested_at,
        source_run_id as _source_run_id

    from source

)

select * from renamed
