{{ config(materialized='view') }}

/*
  Staging for CFPB Consumer Complaints (incremental / append-only landing).
  Casts TEXT -> typed values, normalises Yes/No + True/False flags to booleans,
  and deduplicates on complaint_id keeping the most-recently-ingested record.
*/

with source as (

    select * from {{ source('ripple_raw', 'FED_CFPB_COMPLAINTS') }}

),

renamed_cast as (

    select

        -- primary key
        trim(complaint_id)                                     as complaint_id,

        -- dates (source values are ISO-8601 strings; keep the calendar date)
        try_to_date(left(trim(date_received), 10))            as date_received,
        try_to_date(left(trim(date_sent_to_company), 10))     as date_sent_to_company,

        -- complaint taxonomy
        nullif(trim(product), '')                             as product,
        nullif(trim(sub_product), '')                         as sub_product,
        nullif(trim(issue), '')                               as issue,
        nullif(trim(sub_issue), '')                           as sub_issue,

        -- company + geography (cross-source join keys)
        nullif(trim(company), '')                             as company,
        nullif(trim(state), '')                               as state,
        nullif(trim(zip_code), '')                            as zip_code,

        -- intake + outcome
        nullif(trim(submitted_via), '')                       as submitted_via,
        nullif(trim(company_response), '')                    as company_response,
        nullif(trim(company_public_response), '')             as company_public_response,
        try_to_boolean(trim(timely))                          as is_timely,
        try_to_boolean(trim(has_narrative))                   as has_narrative,
        nullif(trim(tags), '')                                as tags,
        nullif(trim(complaint_what_happened), '')             as complaint_narrative,

        -- pipeline audit columns (_ingested_at lands as epoch-microseconds NUMBER)
        to_timestamp_ntz(_ingested_at, 6)                     as _ingested_at,
        nullif(trim(_source_run_id), '')                      as _source_run_id

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by complaint_id
            order by _ingested_at desc nulls last
        ) as _row_num
    from renamed_cast

)

select
    complaint_id,
    date_received,
    date_sent_to_company,
    product,
    sub_product,
    issue,
    sub_issue,
    company,
    state,
    zip_code,
    submitted_via,
    company_response,
    company_public_response,
    is_timely,
    has_narrative,
    tags,
    complaint_narrative,
    _ingested_at,
    _source_run_id
from deduped
where _row_num = 1
