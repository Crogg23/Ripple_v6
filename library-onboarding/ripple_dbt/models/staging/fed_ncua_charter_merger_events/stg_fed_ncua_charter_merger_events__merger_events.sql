{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_NCUA_CHARTER_MERGER_EVENTS') }}

),

renamed as (

    select

        trim(REGION)                                   as region,
        trim(CONTINUING_CREDIT_UNION_CHARTER)          as continuing_credit_union_charter,
        trim(CONTINUING_NAME)                          as continuing_name,
        trim(CONTINUING_LOCATION)                      as continuing_location,
        try_to_number(trim(CONTINUING_ASSETS))         as continuing_assets,
        trim(MERGING_CREDIT_UNION_CHARTER)             as merging_credit_union_charter,
        trim(MERGING_CREDIT_UNION_NAME)                as merging_credit_union_name,
        trim(MERGING_LOCATION)                         as merging_location,
        try_to_number(trim(MERGING_ASSETS))            as merging_assets,
        trim(MERGING_REASON)                           as merging_reason,
        trim(CONTINUING_FIELD_OF_MEMBERSHIP)           as continuing_field_of_membership,
        trim(MERGING_FIELD_OF_MEMBERSHIP)              as merging_field_of_membership,
        INGESTED_AT                                    as _loaded_at,
        SOURCE_RUN_ID                                  as _source_run_id,
        SRC_SHA256                                     as _src_sha256

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by merging_credit_union_charter
            order by _loaded_at desc
        ) as _row_num
    from renamed
    where merging_credit_union_charter is not null

)

select * exclude (_row_num) from deduped
where _row_num = 1
