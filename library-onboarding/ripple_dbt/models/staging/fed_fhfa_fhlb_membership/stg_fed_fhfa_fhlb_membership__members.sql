{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_FHFA_FHLB_MEMBERSHIP') }}

),

renamed as (

    select

        trim(FHFA_ID)                                  as fhfa_id,
        trim(DISTRICT)                                 as district,
        trim(MEMBER_NAME)                              as member_name,
        trim(CITY)                                     as city,
        trim(STATE)                                    as state,
        trim(ZIP)                                      as zip,
        trim(MEM_TYPE)                                 as mem_type,
        trim(CHAR_TYPE)                                as char_type,
        trim(CERT)                                     as cert,
        trim(FED_ID)                                   as fed_id,
        trim(NCUA_ID)                                  as ncua_id,
        trim(NAIC_ID)                                  as naic_id,
        try_to_date(trim(APPR_DATE), 'MM/DD/YY')       as appr_date,
        try_to_date(trim(MEM_DATE), 'MM/DD/YY')        as mem_date,
        INGESTED_AT                                    as _loaded_at,
        SOURCE_RUN_ID                                  as _source_run_id,
        SRC_SHA256                                     as _src_sha256

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by fhfa_id
            order by _loaded_at desc
        ) as _row_num
    from renamed
    where fhfa_id is not null

)

select * exclude (_row_num) from deduped
where _row_num = 1
