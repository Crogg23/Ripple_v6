{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_SEC_INVESTMENT_COMPANY_SERIES_CLASS') }}

),

keyed as (

    -- CLASS_ID is NEAR-unique (43,122 distinct of 43,123 rows). The single
    -- collision is a genuinely distinct record, not an exact dupe, so a
    -- row_number() over the full-row hash is appended as a deterministic
    -- provenance tiebreaker (fed_fjc_idb_civil idiom).
    select
        source.*,
        {{ dbt_utils.generate_surrogate_key(['CLASS_ID']) }}
            || '-'
            || row_number() over (
                   partition by CLASS_ID
                   order by hash(*)
               ) as series_class_record_id
    from source

),

renamed as (

    select

        series_class_record_id,
        trim(REPORTING_FILE_NUMBER)                    as reporting_file_number,
        trim(CIK_NUMBER)                               as cik_number,
        trim(ENTITY_NAME)                              as entity_name,
        trim(ENTITY_ORG_TYPE)                          as entity_org_type,
        trim(SERIES_ID)                                as series_id,
        trim(SERIES_NAME)                              as series_name,
        trim(CLASS_ID)                                 as class_id,
        trim(CLASS_NAME)                               as class_name,
        trim(CLASS_TICKER)                             as class_ticker,
        trim(ADDRESS_1)                                as address_1,
        trim(ADDRESS_2)                                as address_2,
        trim(CITY)                                     as city,
        trim(STATE)                                    as state,
        trim(ZIP_CODE)                                 as zip_code,
        INGESTED_AT                                    as _loaded_at,
        SOURCE_RUN_ID                                  as _source_run_id,
        SRC_SHA256                                     as _src_sha256

    from keyed

)

select * from renamed
