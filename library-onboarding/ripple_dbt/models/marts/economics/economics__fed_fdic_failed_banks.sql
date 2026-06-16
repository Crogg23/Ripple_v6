{{ config(materialized='table') }}

with base as (

    select * from {{ ref('stg_fed_fdic_failed_banks__failed_banks') }}

),

enriched as (

    select

        -- surrogate / business keys (exposed for cross-source joins)
        fdic_cert,
        fips,
        fdic_failure_record_id,
        financial_institution_number,

        -- institution details
        bank_name,
        city,
        state_abbr,
        state_name,
        city_state,
        charter_type,
        acquiring_institution,

        -- supervision & resolution
        supervisory_agency_code,
        resolution_type,
        resolution_type_detail,

        -- dates
        fail_date,
        insured_date,
        datediff('year', insured_date, fail_date)               as years_insured_before_failure,

        -- financials (in thousands)
        total_assets_thousands,
        total_deposits_thousands,
        estimated_loss_thousands,

        -- derived ratios (guarded against divide-by-zero)
        case
            when total_assets_thousands is not null
             and total_assets_thousands <> 0
            then round(estimated_loss_thousands / total_assets_thousands, 6)
        end                                                     as loss_to_assets_ratio,

        case
            when total_deposits_thousands is not null
             and total_deposits_thousands <> 0
            then round(estimated_loss_thousands / total_deposits_thousands, 6)
        end                                                     as loss_to_deposits_ratio,

        -- flags
        case when acquiring_institution is null
              or upper(trim(acquiring_institution)) in ('NONE', 'N/A', '')
             then true else false
        end                                                     as is_deposit_payoff,

        -- metadata
        _ingested_at,
        _source_run_id

    from base

)

select * from enriched
