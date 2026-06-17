{{ config(materialized='table') }}

with base as (

    select * from {{ ref('stg_fed_cms_hcris__hospital_cost_report') }}

),

enriched as (

    select

        -- surrogate / primary key
        hospital_cost_report_key,

        -- key identifiers for cross-source joins
        provider_number,
        npi,
        fiscal_year,
        fiscal_year_begin_date,
        fiscal_year_end_date,

        -- facility dimensions
        hospital_name,
        street_address,
        city,
        state,
        zip_code,
        county,
        rural_versus_urban,
        type_of_control,

        -- report metadata
        report_status,

        -- utilization
        number_of_beds,
        total_discharges,
        total_patient_days,
        medicare_discharges,
        medicare_days,
        medicaid_days,
        fte_employees,

        -- financials
        total_charges,
        net_revenue,
        total_costs,
        dsh_percent,

        -- derived metrics
        case
            when total_discharges > 0
                then round(total_patient_days / total_discharges, 2)
            else null
        end                                                         as avg_length_of_stay,

        case
            when total_discharges > 0
                then round(medicare_discharges / total_discharges * 100, 2)
            else null
        end                                                         as medicare_discharge_pct,

        case
            when total_patient_days > 0
                then round((medicare_days + medicaid_days) / total_patient_days * 100, 2)
            else null
        end                                                         as government_payer_days_pct,

        case
            when net_revenue > 0
                then round((net_revenue - total_costs) / net_revenue * 100, 2)
            else null
        end                                                         as operating_margin_pct,

        case
            when total_discharges > 0
                then round(total_costs / total_discharges, 2)
            else null
        end                                                         as cost_per_discharge,

        case
            when number_of_beds > 0
                then round(total_patient_days / (number_of_beds * 365) * 100, 2)
            else null
        end                                                         as occupancy_rate_pct,

        -- metadata
        _ingested_at,
        _source_run_id

    from base

)

select * from enriched
