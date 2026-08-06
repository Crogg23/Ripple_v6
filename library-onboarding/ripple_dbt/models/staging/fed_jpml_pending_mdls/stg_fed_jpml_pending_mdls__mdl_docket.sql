{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_JPML_PENDING_MDLS') }}

),

renamed as (

    select

        -- identifiers
        trim(MDL_NO)                                   as mdl_no,

        -- dimensions
        trim(DISTRICT)                                 as district,
        trim(JUDGE)                                    as judge,
        trim(LITIGATION)                               as litigation,

        -- measures
        try_to_number(trim(PENDING))                   as pending_cases,
        try_to_number(trim(TOTAL))                     as total_cases,

        -- metadata
        _ingested_at,
        _source_run_id

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by mdl_no
            order by _ingested_at desc
        ) as _row_num
    from renamed
    where mdl_no is not null

)

select
    district,
    judge,
    mdl_no,
    litigation,
    pending_cases,
    total_cases,
    _ingested_at,
    _source_run_id
from deduped
where _row_num = 1
