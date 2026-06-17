{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'FED_CMS_HCRIS') }}

),

renamed as (

    select

        -- identifiers
        rpt_rec_num                                                        as rpt_rec_num,
        provider_ccn                                                       as provider_ccn,
        hospital_name                                                      as hospital_name,

        -- location
        street_address                                                     as street_address,
        city                                                               as city,
        state_code                                                         as state_code,
        zip_code                                                           as zip_code,
        county                                                             as county,
        medicare_cbsa_number                                               as medicare_cbsa_number,
        rural_versus_urban                                                 as rural_versus_urban,

        -- classification
        ccn_facility_type                                                  as ccn_facility_type,
        provider_type                                                      as provider_type,
        type_of_control                                                    as type_of_control,

        -- dates
        try_to_date(fiscal_year_begin_date)                                as fiscal_year_begin_date,
        try_to_date(fiscal_year_end_date)                                  as fiscal_year_end_date,

        -- workforce
        try_to_double(fte___employees_on_payroll)                          as fte_employees_on_payroll,
        try_to_double(number_of_interns_and_residents__fte)                as number_of_interns_and_residents_fte,

        -- utilization – total
        try_to_number(total_days_title_v)                                  as total_days_title_v,
        try_to_number(total_days_title_xviii)                              as total_days_title_xviii,
        try_to_number(total_days_title_xix)                                as total_days_title_xix,
        try_to_number(total_days__v___xviii___xix___unknown)               as total_days_all,
        try_to_number(number_of_beds)                                      as number_of_beds,
        try_to_number(total_bed_days_available)                            as total_bed_days_available,
        try_to_number(total_discharges_title_v)                            as total_discharges_title_v,
        try_to_number(total_discharges_title_xviii)                        as total_discharges_title_xviii,
        try_to_number(total_discharges_title_xix)                          as total_discharges_title_xix,
        try_to_number(total_discharges__v___xviii___xix___unknown)         as total_discharges_all,
        try_to_number(number_of_beds___total_for_all_subproviders)         as number_of_beds_total_all_subproviders,

        -- utilization – adults & peds
        try_to_number(hospital_total_days_title_v_for_adults___peds)                             as hospital_total_days_title_v_adults_peds,
        try_to_number(hospital_total_days_title_xviii_for_adults___peds)                         as hospital_total_days_title_xviii_adults_peds,
        try_to_number(hospital_total_days_title_xix_for_adults___peds)                           as hospital_total_days_title_xix_adults_peds,
        try_to_number(hospital_total_days__v___xviii___xix___unknown__for_adults___peds)         as hospital_total_days_all_adults_peds,
        try_to_number(hospital_number_of_beds_for_adults___peds)                                 as hospital_number_of_beds_adults_peds,
        try_to_number(hospital_total_bed_days_available_for_adults___peds)                       as hospital_total_bed_days_available_adults_peds,
        try_to_number(hospital_total_discharges_title_v_for_adults___peds)                       as hospital_total_discharges_title_v_adults_peds,
        try_to_number(hospital_total_discharges_title_xviii_for_adults___peds)                   as hospital_total_discharges_title_xviii_adults_peds,
        try_to_number(hospital_total_discharges_title_xix_for_adults___peds)                     as hospital_total_discharges_title_xix_adults_peds,
        try_to_number(hospital_total_discharges__v___xviii___xix___unknown__for_adults___peds)   as hospital_total_discharges_all_adults_peds,

        -- uncompensated care
        try_to_double(cost_of_charity_care)                                as cost_of_charity_care,
        try_to_double(total_bad_debt_expense)                              as total_bad_debt_expense,
        try_to_double(cost_of_uncompensated_care)                          as cost_of_uncompensated_care,
        try_to_double(total_unreimbursed_and_uncompensated_care)           as total_unreimbursed_and_uncompensated_care,

        -- cost structure
        try_to_double(total_salaries_from_worksheet_a)                     as total_salaries_from_worksheet_a,
        try_to_double(overhead_non_salary_costs)                           as overhead_non_salary_costs,
        try_to_double(depreciation_cost)                                   as depreciation_cost,
        try_to_double(total_costs)                                         as total_costs,

        -- charges
        try_to_double(inpatient_total_charges)                             as inpatient_total_charges,
        try_to_double(outpatient_total_charges)                            as outpatient_total_charges,
        try_to_double(combined_outpatient___inpatient_total_charges)       as combined_outpatient_inpatient_total_charges,

        -- wage-related costs
        try_to_double(wage_related_costs__core)                            as wage_related_costs_core,
        try_to_double(wage_related_costs__rhc_fqhc)                        as wage_related_costs_rhc_fqhc,
        try_to_double(total_salaries__adjusted)                            as total_salaries_adjusted,
        try_to_double(contract_labor__direct_patient_care)                 as contract_labor_direct_patient_care,
        try_to_double(wage_related_costs_for_part___a_teaching_physicians) as wage_related_costs_part_a_teaching_physicians,
        try_to_double(wage_related_costs_for_interns_and_residents)        as wage_related_costs_interns_and_residents,

        -- current assets
        try_to_double(cash_on_hand_and_in_banks)                           as cash_on_hand_and_in_banks,
        try_to_double(temporary_investments)                               as temporary_investments,
        try_to_double(notes_receivable)                                    as notes_receivable,
        try_to_double(accounts_receivable)                                 as accounts_receivable,
        try_to_double(less__allowances_for_uncollectible_notes_and_accounts_receivable) as allowances_for_uncollectible_receivables,
        try_to_double(inventory)                                           as inventory,
        try_to_double(prepaid_expenses)                                    as prepaid_expenses,
        try_to_double(other_current_assets)                                as other_current_assets,
        try_to_double(total_current_assets)                                as total_current_assets,

        -- fixed assets
        try_to_double(land)                                                as land,
        try_to_double(land_improvements)                                   as land_improvements,
        try_to_double(buildings)                                           as buildings,
        try_to_double(leasehold_improvements)                              as leasehold_improvements,
        try_to_double(fixed_equipment)                                     as fixed_equipment,
        try_to_double(major_movable_equipment)                             as major_movable_equipment,
        try_to_double(minor_equipment_depreciable)                         as minor_equipment_depreciable,
        try_to_double(health_information_technology_designated_assets)     as health_information_technology_designated_assets,
        try_to_double(total_fixed_assets)                                  as total_fixed_assets,

        -- other assets
        try_to_double(investments)                                         as investments,
        try_to_double(other_assets)                                        as other_assets,
        try_to_double(total_other_assets)                                  as total_other_assets,
        try_to_double(total_assets)                                        as total_assets,

        -- current liabilities
        try_to_double(accounts_payable)                                    as accounts_payable,
        try_to_double(salaries__wages__and_fees_payable)                   as salaries_wages_and_fees_payable,
        try_to_double(payroll_taxes_payable)                               as payroll_taxes_payable,
        try_to_double(notes_and_loans_payable__short_term)                 as notes_and_loans_payable_short_term,
        try_to_double(deferred_income)                                     as deferred_income,
        try_to_double(other_current_liabilities)                           as other_current_liabilities,
        try_to_double(total_current_liabilities)                           as total_current_liabilities,

        -- long-term liabilities
        try_to_double(mortgage_payable)                                    as mortgage_payable,
        try_to_double(notes_payable)                                       as notes_payable,
        try_to_double(unsecured_loans)                                     as unsecured_loans,
        try_to_double(other_long_term_liabilities)                         as other_long_term_liabilities,
        try_to_double(total_long_term_liabilities)                         as total_long_term_liabilities,
        try_to_double(total_liabilities)                                   as total_liabilities,

        -- fund balances
        try_to_double(general_fund_balance)                                as general_fund_balance,
        try_to_double(total_fund_balances)                                 as total_fund_balances,
        try_to_double(total_liabilities_and_fund_balances)                 as total_liabilities_and_fund_balances,

        -- drg / medicare payments
        try_to_double(drg_amounts_other_than_outlier_payments)             as drg_amounts_other_than_outlier_payments,
        try_to_double(drg_amounts_before_october_1)                        as drg_amounts_before_october_1,
        try_to_double(drg_amounts_after_october_1)                         as drg_amounts_after_october_1,
        try_to_double(outlier_payments_for_discharges)                     as outlier_payments_for_discharges,
        try_to_double(disproportionate_share_adjustment)                   as disproportionate_share_adjustment,
        try_to_double(allowable_dsh_percentage)                            as allowable_dsh_percentage,
        try_to_double(managed_care_simulated_payments)                     as managed_care_simulated_payments,
        try_to_double(total_ime_payment)                                   as total_ime_payment,

        -- revenue & income
        try_to_double(inpatient_revenue)                                   as inpatient_revenue,
        try_to_double(outpatient_revenue)                                  as outpatient_revenue,
        try_to_double(total_patient_revenue)                               as total_patient_revenue,
        try_to_double(less_contractual_allowance_and_discounts_on_patients__accounts) as contractual_allowance_and_discounts,
        try_to_double(net_patient_revenue)                                 as net_patient_revenue,
        try_to_double(less_total_operating_expense)                        as total_operating_expense,
        try_to_double(net_income_from_service_to_patients)                 as net_income_from_service_to_patients,
        try_to_double(total_other_income)                                  as total_other_income,
        try_to_double(total_income)                                        as total_income,
        try_to_double(total_other_expenses)                                as total_other_expenses,
        try_to_double(net_income)                                          as net_income,

        -- ratios
        try_to_double(cost_to_charge_ratio)                                as cost_to_charge_ratio,

        -- medicaid
        try_to_double(net_revenue_from_medicaid)                           as net_revenue_from_medicaid,
        try_to_double(medicaid_charges)                                    as medicaid_charges,
        try_to_double(net_revenue_from_stand_alone_chip)                   as net_revenue_from_stand_alone_chip,
        try_to_double(stand_alone_chip_charges)                            as stand_alone_chip_charges,

        -- metadata
        _ingested_at,
        _source_run_id

    from source

),

deduped as (

    select *
    from renamed
    qualify row_number() over (
        partition by provider_ccn, hospital_name, fiscal_year_end_date
        order by _ingested_at desc
    ) = 1

)

select * from deduped
