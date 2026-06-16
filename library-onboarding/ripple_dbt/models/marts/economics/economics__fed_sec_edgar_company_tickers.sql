{{ config(materialized='table') }}

with

staging as (

    select *
    from {{ ref('stg_fed_sec_edgar_company_tickers__company_tickers') }}

),

final as (

    select
        -- primary / foreign key identifiers
        cik,
        ticker,

        -- descriptive attributes
        index_key,
        company_title,

        -- metadata
        _ingested_at,
        _source_run_id

    from staging

)

select *
from final
