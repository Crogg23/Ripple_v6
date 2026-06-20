{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'FED_NOAA_AIS') }}

),

renamed_cast as (

    select

        -- identifiers
        trim(MMSI)                                          as mmsi,
        trim(IMO)                                           as imo_number,
        try_to_date(trim(DATE))                             as date,

        -- timestamps
        try_to_timestamp(trim(BASEDATETIME))                as base_datetime,

        -- position
        try_to_double(trim(LAT))                            as latitude,
        try_to_double(trim(LON))                            as longitude,

        -- navigation
        try_to_double(trim(SOG))                            as speed_over_ground,
        try_to_double(trim(COG))                            as course_over_ground,
        try_to_double(trim(HEADING))                        as heading,

        -- vessel attributes
        trim(VESSELNAME)                                    as vessel_name,
        trim(CALLSIGN)                                      as call_sign,
        try_to_number(trim(VESSELTYPE))                     as vessel_type_code,
        trim(STATUS)                                        as nav_status,
        try_to_double(trim(LENGTH))                         as length_meters,
        try_to_double(trim(WIDTH))                          as width_meters,
        try_to_double(trim(DRAFT))                          as draft_meters,
        try_to_number(trim(CARGO))                          as cargo_type_code,

        -- metadata
        trim(TRANSCEIVER_CLASS)                             as transceiver_class,
        trim(SOURCE_FILE)                                   as source_file,

        -- pipeline audit columns (carry-through if present, else null)
        to_timestamp_ntz(_ingested_at, 6)                   as _ingested_at,
        nullif(trim(try_cast(_source_run_id as text)), '') as _source_run_id

    from source

),

deduped as (

    select
        *,
        row_number() over (
            partition by mmsi, imo_number, date, base_datetime
            order by _ingested_at nulls last
        ) as _row_num
    from renamed_cast

)

select * exclude (_row_num)
from deduped
where _row_num = 1
