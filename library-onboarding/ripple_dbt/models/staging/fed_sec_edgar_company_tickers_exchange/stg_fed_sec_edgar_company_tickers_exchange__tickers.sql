{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE') }}

),

renamed as (

    select

        -- identifiers
        -- (CIK, TICKER) is the verified-unique grain (10,398 rows). CIK is the
        -- SEC Central Index Key — THE join key to all other SEC data (EDGAR
        -- filings, DERA submissions, 13F, insider filings).
        try_to_number(cast(CIK as varchar))            as cik,
        trim(TICKER)                                   as ticker,
        try_to_number(cast(CIK as varchar)) || '-' || trim(TICKER)
                                                       as cik_ticker,

        -- dimensions
        trim(NAME)                                     as company_name,
        trim(EXCHANGE)                                 as exchange,

        -- metadata (no-underscore landing metadata columns)
        INGESTED_AT                                    as _loaded_at,
        SOURCE_RUN_ID                                  as _source_run_id,
        SRC_SHA256                                     as _src_sha256

    from source

)

select * from renamed
