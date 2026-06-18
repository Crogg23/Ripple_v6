{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'INTL_IE_CRO') }}

),

renamed as (

    select
        -- key identifiers
        COMPANY_ID                                          as company_id,
        COUNTRY                                             as country,

        -- descriptive attributes
        COMPANY_NAME                                        as company_name,
        COMPANY_STATUS                                      as company_status,
        COMPANY_TYPE                                        as company_type,
        REGISTERED_ADDRESS                                  as registered_address,
        DATASET_NAME                                        as dataset_name,

        -- date columns
        try_to_date(INCORPORATION_DATE, 'YYYY-MM-DD')       as incorporation_date,
        try_to_date(FINANCIAL_YEAR_END, 'YYYY-MM-DD')       as financial_year_end,

        -- metadata
        _ingested_at,
        _source_run_id

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by company_id, country
            order by _ingested_at desc
        ) as _row_num
    from renamed

)

select
    company_id,
    country,
    company_name,
    company_status,
    company_type,
    registered_address,
    dataset_name,
    incorporation_date,
    financial_year_end,
    _ingested_at,
    _source_run_id
from deduped
where _row_num = 1
