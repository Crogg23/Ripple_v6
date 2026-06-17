{{ config(materialized='view') }}

with source as (

    select *
    from {{ source('ripple_raw', 'FED_DOJ_CRT_CASES') }}

),

renamed as (

    select
        -- identifiers & keys
        DEFENDANT_COMPANY_ID                                    as company_id,
        PERSON_NAME                                             as person_name,
        STATE                                                   as state,

        -- case descriptors
        CASE_TITLE                                              as case_title,
        SECTION                                                 as section,
        CASE_TYPE                                               as case_type,
        STATUS                                                  as status,
        SUMMARY                                                 as summary,
        CASE_URL                                                as case_url,

        -- dates
        try_to_date(DATE_FILED,    'YYYY-MM-DD')                as date_filed,
        try_to_date(DATE_RESOLVED, 'YYYY-MM-DD')                as date_resolved,
        try_to_date(DATE_UPDATED,  'YYYY-MM-DD')                as date_updated,

        -- financials
        try_to_double(replace(replace(SETTLEMENT_AMOUNT, '$', ''), ',', '')) as settlement_amount,

        -- metadata
        _ingested_at,
        _source_run_id

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by
                company_id,
                person_name,
                state,
                date_filed
            order by _ingested_at desc
        ) as _row_num
    from renamed

)

select
    company_id,
    person_name,
    state,
    case_title,
    section,
    case_type,
    status,
    summary,
    case_url,
    date_filed,
    date_resolved,
    date_updated,
    settlement_amount,
    _ingested_at,
    _source_run_id
from deduped
where _row_num = 1
