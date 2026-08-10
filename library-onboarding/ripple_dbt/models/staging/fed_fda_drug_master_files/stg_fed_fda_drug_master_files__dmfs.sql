{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_FDA_DRUG_MASTER_FILES') }}

),

renamed as (

    select

        -- identifiers
        trim(DMF)                                      as dmf_number,

        -- dimensions
        trim(STATUS)                                   as status_code,
        case trim(STATUS)
            when 'A' then 'Active'
            when 'I' then 'Inactive'
            else trim(STATUS)
        end                                            as status,
        trim(TYPE)                                     as dmf_type,
        -- SUBMIT_DATE arrives as 'YYYY-MM-DD HH24:MI:SS'
        try_to_date(trim(SUBMIT_DATE), 'YYYY-MM-DD HH24:MI:SS')
                                                       as submit_date,
        trim(HOLDER)                                   as holder,
        trim(SUBJECT)                                  as subject,

        -- metadata
        to_timestamp_ntz(INGESTED_AT, 6)               as _ingested_at,
        SOURCE_RUN_ID                                  as _source_run_id,
        SRC_SHA256                                     as _src_sha256

    from source

)

select * from renamed
