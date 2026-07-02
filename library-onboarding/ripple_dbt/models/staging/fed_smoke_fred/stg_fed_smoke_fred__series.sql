{{ config(materialized='view') }}

with source as (
    select * from {{ source('ripple_raw', 'FED_SMOKE_FRED') }}
),
renamed as (
    select
        series_id::varchar     as series_id,
        try_to_date(date)      as observation_date,
        try_to_double(value)   as value,
        _ingested_at,
        _source_run_id
    from source
)
select * from renamed
