{{ config(materialized='view') }}

with

source as (

    select *
    from {{ source('ripple_raw', 'FED_SEC_EDGAR_COMPANY_TICKERS') }}

),

renamed as (

    select
        -- keys
        try_to_number(index_key)          as index_key,
        try_to_number(cik_str)            as cik,
        trim(ticker)                      as ticker,

        -- attributes
        trim(title)                       as company_title,

        -- metadata
        _ingested_at,
        _source_run_id

    from source

),

deduped as (

    select *
    from renamed
    qualify row_number() over (
        partition by cik, ticker
        order by _ingested_at desc
    ) = 1

)

select *
from deduped
