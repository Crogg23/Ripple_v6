{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_EPA_AQS_SITES') }}

),

renamed as (

    select

        trim(STATE_CODE) || '-' || trim(COUNTY_CODE) || '-' || trim(SITE_NUMBER) as aqs_site_id,
        trim(STATE_CODE)                               as state_code,
        trim(COUNTY_CODE)                              as county_code,
        trim(SITE_NUMBER)                              as site_number,
        try_to_number(trim(LATITUDE))                  as latitude,
        try_to_number(trim(LONGITUDE))                 as longitude,
        trim(DATUM)                                    as datum,
        try_to_number(trim(ELEVATION))                 as elevation,
        trim(LAND_USE)                                 as land_use,
        trim(LOCATION_SETTING)                         as location_setting,
        try_to_date(trim(SITE_ESTABLISHED_DATE), 'YYYY-MM-DD') as site_established_date,
        try_to_date(trim(SITE_CLOSED_DATE), 'YYYY-MM-DD') as site_closed_date,
        trim(MET_SITE_STATE_CODE)                      as met_site_state_code,
        trim(MET_SITE_COUNTY_CODE)                     as met_site_county_code,
        trim(MET_SITE_SITE_NUMBER)                     as met_site_site_number,
        trim(MET_SITE_TYPE)                            as met_site_type,
        try_to_number(trim(MET_SITE_DISTANCE))         as met_site_distance,
        trim(MET_SITE_DIRECTION)                       as met_site_direction,
        try_to_number(trim(GMT_OFFSET))                as gmt_offset,
        trim(OWNING_AGENCY)                            as owning_agency,
        trim(LOCAL_SITE_NAME)                          as local_site_name,
        trim(ADDRESS)                                  as address,
        trim(ZIP_CODE)                                 as zip_code,
        trim(STATE_NAME)                               as state_name,
        trim(COUNTY_NAME)                              as county_name,
        trim(CITY_NAME)                                as city_name,
        trim(CBSA_NAME)                                as cbsa_name,
        trim(TRIBE_NAME)                               as tribe_name,
        try_to_date(trim(EXTRACTION_DATE), 'YYYY-MM-DD') as extraction_date,
        INGESTED_AT                                    as _loaded_at,
        SOURCE_RUN_ID                                  as _source_run_id,
        SRC_SHA256                                     as _src_sha256

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by aqs_site_id
            order by _loaded_at desc
        ) as _row_num
    from renamed
    where aqs_site_id is not null

)

select * exclude (_row_num) from deduped
where _row_num = 1
