{{ config(materialized='table') }}

with base as (

    select *
    from {{ ref('stg_fed_doj_crt_cases__crt_cases') }}

)

select

    -- surrogate / join keys exposed for cross-source joins
    {{ dbt_utils.generate_surrogate_key([
        'company_id',
        'person_name',
        'state',
        'date_filed'
    ]) }}                                       as crt_case_key,

    company_id,
    person_name,
    state,

    -- case details
    case_title,
    section,
    case_type,
    status,
    summary,
    case_url,

    -- dates
    date_filed,
    date_resolved,
    date_updated,

    -- financials
    settlement_amount,

    -- derived helpers
    case
        when settlement_amount is not null and settlement_amount > 0
            then true
        else false
    end                                         as has_monetary_settlement,

    datediff(
        'day',
        date_filed,
        coalesce(date_resolved, current_date())
    )                                           as days_to_resolution,

    case
        when date_resolved is not null then 'closed'
        else 'open'
    end                                         as case_open_closed,

    -- metadata
    _ingested_at,
    _source_run_id

from base
