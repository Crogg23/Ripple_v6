{{ config(materialized='table') }}

with base as (

    select * from {{ ref('stg_fed_cms_hpt_enforcement__hospital_price_transparency_enforcement') }}

),

final as (

    select
        -- surrogate key
        {{ dbt_utils.generate_surrogate_key(['npi', 'hospital_name', 'action_date', 'enforcement_action_type']) }}
                                                        as enforcement_action_key,

        -- key identifiers (exposed for cross-source joins)
        npi,
        hospital_name,

        -- location
        city,
        state,

        -- enforcement details
        enforcement_action_type,
        action_date,
        outcome,
        penalty_amount,
        corrective_action_plan,
        compliance_status,

        -- derived flags
        case
            when penalty_amount is not null and penalty_amount > 0 then true
            else false
        end                                             as has_civil_monetary_penalty,

        case
            when upper(trim(corrective_action_plan)) in ('YES', 'Y', 'TRUE', '1') then true
            when upper(trim(corrective_action_plan)) in ('NO', 'N', 'FALSE', '0') then false
            else null
        end                                             as requires_corrective_action_plan,

        case
            when lower(compliance_status) like '%compliant%'
             and lower(compliance_status) not like '%non%' then 'compliant'
            when lower(compliance_status) like '%non%compliant%' then 'non-compliant'
            when lower(compliance_status) like '%pending%' then 'pending'
            else compliance_status
        end                                             as compliance_status_normalized,

        -- metadata
        _ingested_at,
        _source_run_id

    from base

)

select * from final
