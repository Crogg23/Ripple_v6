{{ config(materialized='view') }}

with source as (

    select *
    from {{ source('ripple_raw', 'FED_NAAG_MULTISTATE_SETTLEMENTS') }}

),

renamed_cast as (

    select
        -- key identifiers
        company_id                                        as company_id,
        try_to_date(date, 'YYYY-MM-DD')                   as date,
        state                                             as state,

        -- descriptive attributes
        company_name                                      as company_name,
        try_to_double(settlement_amount)                  as settlement_amount,
        case_description                                  as case_description,
        industry                                          as industry,
        lead_state                                        as lead_state,
        try_to_number(num_states)                         as num_states,
        document_url                                      as document_url,

        -- metadata
        _ingested_at                                      as _ingested_at,
        _source_run_id                                    as _source_run_id

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by company_id, date, state
            order by _ingested_at desc
        ) as _row_num
    from renamed_cast

)

select
    company_id,
    date,
    state,
    company_name,
    settlement_amount,
    case_description,
    industry,
    lead_state,
    num_states,
    document_url,
    _ingested_at,
    _source_run_id
from deduped
where _row_num = 1
