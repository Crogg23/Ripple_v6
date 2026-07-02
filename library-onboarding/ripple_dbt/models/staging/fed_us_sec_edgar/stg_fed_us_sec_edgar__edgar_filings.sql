{{ config(materialized='view') }}

with source as (

    select *
    from {{ source('ripple_raw', 'FED_US_SEC_EDGAR') }}

),

renamed as (

    select

        -- primary key
        accession_number                                        as accession_number,

        -- identifiers
        cik                                                     as cik,
        ticker                                                  as ticker,
        isin                                                    as isin,
        ein                                                     as ein,

        -- entity attributes
        entity_name                                             as entity_name,
        form_type                                               as form_type,
        sic_code                                                as sic_code,
        state_of_incorporation                                  as state_of_incorporation,
        business_address                                        as business_address,

        -- dates
        try_to_date(filed_at)                                   as filed_at,
        try_to_date(period_of_report)                           as period_of_report,

        -- urls
        filing_url                                              as filing_url,
        document_url                                            as document_url,

        -- metadata
        _ingested_at,
        _source_run_id

    from source

),

deduped as (

    select *
    from (
        select
            *,
            row_number() over (
                partition by accession_number
                order by _ingested_at desc
            ) as _row_num
        from renamed
    )
    where _row_num = 1

)

select
    accession_number,
    cik,
    ticker,
    isin,
    ein,
    entity_name,
    form_type,
    sic_code,
    state_of_incorporation,
    business_address,
    filed_at,
    period_of_report,
    filing_url,
    document_url,
    _ingested_at,
    _source_run_id
from deduped
