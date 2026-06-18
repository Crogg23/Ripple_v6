{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_DOJ_CRT_CASES') }}

),

renamed_cast as (

    select

        -- identifiers & dimensions
        CASE_TITLE                                        as case_title,
        SECTION                                           as section,
        CASE_TYPE                                         as case_type,
        COMPANY_ID                                        as company_id,
        PERSON_NAME                                       as person_name,
        try_to_date(DATE)                                 as date,
        STATE                                             as state,

        -- descriptive
        DOCUMENT_URL                                      as document_url,
        DESCRIPTION                                       as description,
        STATUS                                            as status,

        -- meta
        _ingested_at,
        _source_run_id

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by company_id, person_name, date, state
            order by _ingested_at desc
        ) as _row_num
    from renamed_cast

)

select
    case_title,
    section,
    case_type,
    company_id,
    person_name,
    date,
    state,
    document_url,
    description,
    status,
    _ingested_at,
    _source_run_id
from deduped
where _row_num = 1
