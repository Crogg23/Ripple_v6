{{ config(materialized='table') }}

with base as (

    select * from {{ ref('stg_intl_ie_cro__cro_companies') }}

)

select
    -- surrogate / natural keys
    {{ dbt_utils.generate_surrogate_key(['company_id', 'country']) }}   as corporate_registry_key,
    company_id,
    country,

    -- company profile
    company_name,
    company_status,
    company_type,
    registered_address,

    -- temporal
    incorporation_date,
    financial_year_end,

    -- derived convenience fields
    year(incorporation_date)                                             as incorporation_year,
    datediff('year', incorporation_date, current_date())                as company_age_years,

    -- source lineage
    'intl_ie_cro'                                                        as source_id,
    dataset_name,
    _ingested_at,
    _source_run_id

from base
