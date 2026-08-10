{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'INTL_ISO_MIC_REGISTRY') }}

),

renamed as (

    select

        trim(MIC)                                      as mic,
        trim(OPERATING_MIC)                            as operating_mic,
        trim(OPRT_SGMT)                                as oprt_sgmt,
        trim(MARKET_NAME_INSTITUTION_DESCRIPTION)      as market_name_institution_description,
        trim(LEGAL_ENTITY_NAME)                        as legal_entity_name,
        trim(LEI)                                      as lei,
        trim(MARKET_CATEGORY_CODE)                     as market_category_code,
        trim(ACRONYM)                                  as acronym,
        trim(ISO_COUNTRY_CODE_ISO_3166)                as iso_country_code_iso_3166,
        trim(CITY)                                     as city,
        trim(WEBSITE)                                  as website,
        trim(STATUS)                                   as status,
        try_to_date(trim(CREATION_DATE), 'YYYYMMDD')   as creation_date,
        try_to_date(trim(LAST_UPDATE_DATE), 'YYYYMMDD') as last_update_date,
        try_to_date(trim(LAST_VALIDATION_DATE), 'YYYYMMDD') as last_validation_date,
        try_to_date(trim(EXPIRY_DATE), 'YYYYMMDD')     as expiry_date,
        trim(COMMENTS)                                 as comments,
        INGESTED_AT                                    as _loaded_at,
        SOURCE_RUN_ID                                  as _source_run_id,
        SRC_SHA256                                     as _src_sha256

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by mic
            order by _loaded_at desc
        ) as _row_num
    from renamed
    where mic is not null

)

select * exclude (_row_num) from deduped
where _row_num = 1
