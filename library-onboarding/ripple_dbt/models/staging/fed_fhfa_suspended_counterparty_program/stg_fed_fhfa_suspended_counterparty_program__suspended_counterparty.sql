{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'FED_FHFA_SUSPENDED_COUNTERPARTY_PROGRAM') }}

),

renamed as (

    select
        -- identifiers
        LAST_NAME                                          as last_name,
        COMPANY                                            as company,

        -- descriptive fields
        FIRST_NAME                                         as first_name,
        CITY                                               as city,
        STATE                                              as state,

        -- dates
        try_to_date(EFFECTIVE_DATESORT_ASCENDING)          as effective_date,
        try_to_date(SUSPENSION_END_DATE)                   as suspension_end_date,

        -- other fields
        SUSPENSION_ORDER                                   as suspension_order,

        -- metadata
        _ingested_at,
        _source_run_id

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by last_name, company
            order by _ingested_at desc
        ) as _row_num
    from renamed

)

select
    last_name,
    company,
    first_name,
    city,
    state,
    effective_date,
    suspension_end_date,
    suspension_order,
    _ingested_at,
    _source_run_id
from deduped
where _row_num = 1
