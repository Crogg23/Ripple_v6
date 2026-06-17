{{ config(materialized='table') }}

with base as (

    select * from {{ ref('stg_fed_cms_hcris__hospital_cost_report') }}

)

select

    -- key identifiers
    provider_ccn,
    hospital_name,
    fiscal_year_end_date,
    rpt_rec_num,

    -- location
    street_address,
    city,
    state_code,
    zip_code,
    county,
    medicare_cbsa_number,
    rural_versus_urban,

    -- classification
    ccn_facility_type,
    provider_type,
    type_of_control,

    -- fiscal period
    fiscal_year_begin_date,
    fiscal_year_end_date                                                    as fiscal_year_end_date_key,
    datediff('day', fiscal_year_begin_date, fiscal_year_end_date)           as fiscal_year_length_days,

    -- workforce
    fte_employees_on_payroll,
    number_of_interns_and_residents_fte,

    -- utilization
    number_of_beds,
    total_bed_days_available,
    total_days_title_v,
    total_days_title_xviii,
    total_days_title_xix,
    total_days_all,
    total_discharges_title_v,
    total_discharges_title_xviii,
    total_discharges_title_xix,
    total_discharges_all,
    number_of_beds_total_all_subproviders,
    hospital_number_of_beds_adults_peds,
    hospital_total_bed_days_available_adults_peds,
    hospital_total_days_title_v_adults_peds,
    hospital_total_days_title_xviii_adults_peds,
    hospital_total_days_title_xix_adults_peds,
    hospital_total_days_all_adults_peds,
    hospital_total_discharges_title_v_adults_peds,
    hospital_total_discharges_title_xviii_adults_peds,
    hospital_total_discharges_title_xix_adults_peds,
    hospital_total_discharges_all_adults_peds,

    -- derived utilization metrics
    case
        when total_bed_days_available > 0
        then round(total_days_all / total_bed_days_available, 4)
    end                                                                     as occupancy_rate,

    -- uncompensated care
    cost_of_charity_care,
    total_bad_debt_expense,
    cost_of_uncompensated_care,
    total_unreimbursed_and_uncompensated_care,

    -- cost structure
    total_salaries_from_worksheet_a,
    total_salaries_adjusted,
    overhead_non_salary_costs,
    depreciation_cost,
    total_costs,
    wage_related_costs_core,
    wage_related_costs_rhc_fqhc,
    contract_labor_direct_patient_care,
    wage_related_costs_part_a_teaching_physicians,
    wage_related_costs_interns_and_residents,

    -- charges
    inpatient_total_charges,
    outpatient_total_charges,
    combined_outpatient_inpatient_total_charges,
    cost_to_charge_ratio,

    -- balance sheet – assets
    cash_on_hand_and_in_banks,
    temporary_investments,
    notes_receivable,
    accounts_receivable,
    allowances_for_uncollectible_receivables,
    inventory,
    prepaid_expenses,
    other_current_assets,
    total_current_assets,
    land,
    land_improvements,
    buildings,
    leasehold_improvements,
    fixed_equipment,
    major_movable_equipment,
    minor_equipment_depreciable,
    health_information_technology_designated_assets,
    total_fixed_assets,
    investments,
    other_assets,
    total_other_assets,
    total_assets,

    -- balance sheet – liabilities
    accounts_payable,
    salaries_wages_and_fees_payable,
    payroll_taxes_payable,
    notes_and_loans_payable_short_term,
    deferred_income,
    other_current_liabilities,
    total_current_liabilities,
    mortgage_payable,
    notes_payable,
    unsecured_loans,
    other_long_term_liabilities,
    total_long_term_liabilities,
    total_liabilities,
    general_fund_balance,
    total_fund_balances,
    total_liabilities_and_fund_balances,

    -- derived balance sheet
    case
        when total_current_liabilities > 0
        then round(total_current_assets / total_current_liabilities, 4)
    end                                                                     as current_ratio,

    -- medicare drg / payments
    drg_amounts_other_than_outlier_payments,
    drg_amounts_before_october_1,
    drg_amounts_after_october_1,
    outlier_payments_for_discharges,
    disproportionate_share_adjustment,
    allowable_dsh_percentage,
    managed_care_simulated_payments,
    total_ime_payment,

    -- revenue & income
    inpatient_revenue,
    outpatient_revenue,
    total_patient_revenue,
    contractual_allowance_and_discounts,
    net_patient_revenue,
    total_operating_expense,
    net_income_from_service_to_patients,
    total_other_income,
    total_income,
    total_other_expenses,
    net_income,

    -- medicaid
    net_revenue_from_medicaid,
    medicaid_charges,
    net_revenue_from_stand_alone_chip,
    stand_alone_chip_charges,

    -- derived margin
    case
        when total_patient_revenue > 0
        then round(net_income / total_patient_revenue, 4)
    end                                                                     as net_margin_ratio,

    -- source metadata
    'fed_cms_hcris'                                                         as source_id,
    _ingested_at,
    _source_run_id

from base
