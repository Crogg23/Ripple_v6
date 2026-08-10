{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_OCC_NATIONAL_BANKS') }}

),

renamed as (

    select

        trim(CHARTER_NO)                               as charter_no,
        trim(NAME)                                     as name,
        trim(ADDRESS_LOC)                              as address_loc,
        trim(CITY)                                     as city,
        trim(STATE)                                    as state,
        try_to_number(trim(CERT))                      as cert,
        try_to_number(trim(RSSD))                      as rssd,
        _INGESTED_AT                                   as _loaded_at,
        _SOURCE_RUN_ID                                 as _source_run_id,
        _SRC_SHA256                                    as _src_sha256

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by charter_no
            order by _loaded_at desc
        ) as _row_num
    from renamed
    where charter_no is not null

)

select * exclude (_row_num) from deduped
where _row_num = 1
