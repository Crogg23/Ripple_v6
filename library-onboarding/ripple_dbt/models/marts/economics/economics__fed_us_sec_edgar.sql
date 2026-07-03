{{ config(materialized='table') }}

with base as (

    select *
    from {{ ref('stg_fed_us_sec_edgar__edgar_filings') }}

),

final as (

    select

        -- surrogate / primary key
        accession_number,

        -- cross-source join identifiers
        cik,
        ticker,
        isin,
        ein,

        -- entity attributes
        entity_name,
        form_type,
        sic_code,
        state_of_incorporation,
        business_address,

        -- dates
        filed_at,
        period_of_report,
        year(filed_at)                                          as filed_year,
        month(filed_at)                                         as filed_month,

        -- urls
        filing_url,
        document_url,

        -- derived flags
        case
            when form_type ilike 'S-%'
                 or form_type ilike 'F-%'
                 or form_type in ('424B1','424B2','424B3','424B4',
                                  '424B5','424B7','424B8')
            then true
            else false
        end                                                     as is_registration_or_prospectus,

        case
            when form_type in ('10-K','10-K/A','20-F','20-F/A','40-F','40-F/A')
            then true
            else false
        end                                                     as is_annual_report,

        case
            when form_type in ('10-Q','10-Q/A')
            then true
            else false
        end                                                     as is_quarterly_report,

        -- source metadata
        'fed_us_sec_edgar'                                      as source_id,
        _ingested_at,
        _source_run_id

    from base

)

select * from final
