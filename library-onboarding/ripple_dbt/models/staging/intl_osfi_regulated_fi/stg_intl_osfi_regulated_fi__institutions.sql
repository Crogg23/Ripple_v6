{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'INTL_OSFI_REGULATED_FI') }}

),

keyed as (

    -- The composite (COMPANY_NAME, FI_TYPE_NAME) is NEAR-unique (342 distinct of
    -- 343 rows). The single collision is a genuinely distinct record, not an
    -- exact dupe, so a row_number() over the full-row hash is appended as a
    -- deterministic provenance tiebreaker (fed_fjc_idb_civil idiom).
    select
        source.*,
        {{ dbt_utils.generate_surrogate_key(['COMPANY_NAME', 'FI_TYPE_NAME']) }}
            || '-'
            || row_number() over (
                   partition by COMPANY_NAME, FI_TYPE_NAME
                   order by hash(*)
               ) as osfi_fi_record_id
    from source

),

renamed as (

    select

        osfi_fi_record_id,
        trim(COMPANY_NAME)                             as company_name,
        trim(FI_TYPE_NAME)                             as fi_type_name,
        trim(FI_GROUP_NAME)                            as fi_group_name,
        trim(FI_INDUSTRY_NAME)                         as fi_industry_name,
        trim(CANADIAN_TRADE_COMPANY_NAME)              as canadian_trade_company_name,
        trim(REPRESENTATIVE_NAME)                      as representative_name,
        trim(TITLE)                                    as title,
        trim(ADDRESS_LINE_1)                           as address_line_1,
        trim(ADDRESS_LINE_2)                           as address_line_2,
        trim(CITY)                                     as city,
        trim(PROVINCE_STATE)                           as province_state,
        trim(POSTAL_ZIP_CODE)                          as postal_zip_code,
        trim(AUTHORIZED_INSURANCE_CLASSES)             as authorized_insurance_classes,
        INGESTED_AT                                    as _loaded_at,
        SOURCE_RUN_ID                                  as _source_run_id,
        SRC_SHA256                                     as _src_sha256

    from keyed

)

select * from renamed
