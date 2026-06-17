{{ config(materialized='table') }}

with base as (

    select *
    from {{ ref('stg_fed_naag_multistate_settlements__multistate_settlements') }}

),

final as (

    select
        -- surrogate / natural key components
        {{ dbt_utils.generate_surrogate_key(['company_id', 'date', 'state']) }}
                                                          as settlement_sk,
        company_id,
        date                                              as settlement_date,
        state                                             as state,

        -- settlement details
        company_name,
        settlement_amount,
        case_description,
        industry,
        lead_state,
        num_states,
        document_url,

        -- derived convenience columns
        year(date)                                        as settlement_year,
        month(date)                                       as settlement_month,
        iff(lead_state = state, true, false)              as is_lead_state_row,

        -- metadata
        _ingested_at,
        _source_run_id

    from base

)

select *
from final
