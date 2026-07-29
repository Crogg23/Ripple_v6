{{ config(materialized='view') }}

/*
  2026-07-28 fix: this model was written against an older INTL_IE_CRO raw schema
  (COMPANY_ID, COUNTRY, REGISTERED_ADDRESS, DATASET_NAME, FINANCIAL_YEAR_END --
  none of which exist on the table anymore) and had been silently broken (errors
  on any rebuild) since that raw schema drifted; a stale copy under a personal
  DBT_CROGERS schema was carrying the mart in the meantime and turned out, on
  inspection, to just be a raw passthrough (identical columns to landing), not a
  real rebuild. Remapped to the current columns (confirmed live):
  COMPANY_NUM, COMPANY_NAME, COMPANY_STATUS(_CODE), COMPANY_TYPE(_CODE),
  COMPANY_REG_DATE, COMP_DISSOLVED_DATE, LAST_AR_DATE, LAST_ACCOUNTS_DATE,
  COMPANY_ADDRESS_1..4, EIRCODE. This is an Ireland-only source (no COUNTRY
  column ever existed downstream of the raw feed) so country is a fixed 'IE'.
  There is no longer a recurring "financial year end" field -- LAST_ACCOUNTS_DATE
  (date the last annual accounts were filed) is the closest available proxy.
  DATASET_NAME has no current raw equivalent; left null rather than fabricated.
*/

with source as (

    select * from {{ source('ripple_raw', 'INTL_IE_CRO') }}

),

renamed as (

    select
        -- key identifiers
        trim(COMPANY_NUM)                                   as company_id,
        'IE'                                                 as country,

        -- descriptive attributes
        trim(COMPANY_NAME)                                  as company_name,
        trim(COMPANY_STATUS)                                as company_status,
        trim(COMPANY_TYPE)                                  as company_type,
        nullif(array_to_string(
            array_compact(array_construct(
                nullif(trim(COMPANY_ADDRESS_1), ''),
                nullif(trim(COMPANY_ADDRESS_2), ''),
                nullif(trim(COMPANY_ADDRESS_3), ''),
                nullif(trim(COMPANY_ADDRESS_4), ''),
                nullif(trim(EIRCODE), '')
            )), ', '), '')                                  as registered_address,
        cast(null as varchar)                               as dataset_name,

        -- date columns
        try_to_date(trim(COMPANY_REG_DATE), 'YYYY-MM-DD')      as incorporation_date,
        try_to_date(trim(LAST_ACCOUNTS_DATE), 'YYYY-MM-DD')    as financial_year_end,

        -- metadata
        to_timestamp_ntz(_INGESTED_AT, 6)                   as _ingested_at,
        nullif(trim(_SOURCE_RUN_ID), '')                    as _source_run_id

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
