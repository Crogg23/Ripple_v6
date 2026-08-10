{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_ICE_DETENTION_FACILITY_CODES') }}

),

renamed as (

    select

        trim(DETENTION_FACILITY_CODE)                  as detention_facility_code,
        trim(DETENTION_FACILITY_NAME)                  as detention_facility_name,
        trim(ADDRESS)                                  as address,
        trim(CITY)                                     as city,
        trim(COUNTY)                                   as county,
        trim(STATE)                                    as state,
        trim(ZIP)                                      as zip,
        trim(AOR)                                      as aor,
        try_to_number(trim(LATITUDE))                  as latitude,
        try_to_number(trim(LONGITUDE))                 as longitude,
        trim(TYPE_DETAILED)                            as type_detailed,
        trim(TYPE_GROUPED)                             as type_grouped,
        INGESTED_AT                                    as _loaded_at,
        SOURCE_RUN_ID                                  as _source_run_id,
        SRC_SHA256                                     as _src_sha256

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by detention_facility_code
            order by _loaded_at desc
        ) as _row_num
    from renamed
    where detention_facility_code is not null

)

select * exclude (_row_num) from deduped
where _row_num = 1
