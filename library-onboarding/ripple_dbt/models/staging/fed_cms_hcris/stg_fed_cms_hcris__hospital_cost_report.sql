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
        source_file_year                                                   as source_file_year,

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
        {{ stg_date('fiscal_year_begin_date') }}                                as fiscal_year_begin_date,
        {{ stg_date('fiscal_year_end_date') }}                                  as fiscal_year_end_date,

        -- workforce
        {{ stg_float('fte_employees_on_payroll') }}                          as fte_employees_on_payroll,
        {{ stg_float('number_of_interns_and_residents_fte') }}                as number_of_interns_and_residents_fte,

        -- utilization – total
        {{ stg_int('total_days_title_v') }}                                  as total_days_title_v,
        {{ stg_int('total_days_title_xviii') }}                              as total_days_title_xviii,
        {{ stg_int('total_days_title_xix') }}                                as total_days_title_xix,
        {{ stg_int('total_days_v_xviii_xix_unknown') }}               as total_days_all,
        {{ stg_int('number_of_beds') }}                                      as number_of_beds,
        {{ stg_int('total_bed_days_available') }}                            as total_bed_days_available,
        {{ stg_int('total_discharges_title_v') }}                            as total_discharges_title_v,
        {{ stg_int('total_discharges_title_xviii') }}                        as total_discharges_title_xviii,
        {{ stg_int('total_discharges_title_xix') }}                          as total_discharges_title_xix,
        {{ stg_int('total_discharges_v_xviii_xix_unknown') }}         as total_discharges_all,
        {{ stg_int('number_of_beds_total_for_all_subproviders') }}         as number_of_beds_total_all_subproviders,

        -- utilization – adults & peds
        {{ stg_int('hospital_total_days_title_v_for_adults_peds') }}                             as hospital_total_days_title_v_adults_peds,
        {{ stg_int('hospital_total_days_title_xviii_for_adults_peds') }}                         as hospital_total_days_title_xviii_adults_peds,
        {{ stg_int('hospital_total_days_title_xix_for_adults_peds') }}                           as hospital_total_days_title_xix_adults_peds,
        {{ stg_int('hospital_total_days_v_xviii_xix_unknown_for_adults_peds') }}         as hospital_total_days_all_adults_peds,
        {{ stg_int('hospital_number_of_beds_for_adults_peds') }}                                 as hospital_number_of_beds_adults_peds,
        {{ stg_int('hospital_total_bed_days_available_for_adults_peds') }}                       as hospital_total_bed_days_available_adults_peds,
        {{ stg_int('hospital_total_discharges_title_v_for_adults_peds') }}                       as hospital_total_discharges_title_v_adults_peds,
        {{ stg_int('hospital_total_discharges_title_xviii_for_adults_peds') }}                   as hospital_total_discharges_title_xviii_adults_peds,
        {{ stg_int('hospital_total_discharges_title_xix_for_adults_peds') }}                     as hospital_total_discharges_title_xix_adults_peds,
        {{ stg_int('hospital_total_discharges_v_xviii_xix_unknown_for_adults_peds') }}   as hospital_total_discharges_all_adults_peds,

        -- uncompensated care
        {{ stg_float('cost_of_charity_care') }}                                as cost_of_charity_care,
        {{ stg_float('total_bad_debt_expense') }}                              as total_bad_debt_expense,
        {{ stg_float('cost_of_uncompensated_care') }}                          as cost_of_uncompensated_care,
        {{ stg_float('total_unreimbursed_and_uncompensated_care') }}           as total_unreimbursed_and_uncompensated_care,

        -- cost structure
        {{ stg_float('total_salaries_from_worksheet_a') }}                     as total_salaries_from_worksheet_a,
        {{ stg_float('overhead_non_salary_costs') }}                           as overhead_non_salary_costs,
        {{ stg_float('depreciation_cost') }}                                   as depreciation_cost,
        {{ stg_float('total_costs') }}                                         as total_costs,

        -- charges
        {{ stg_float('inpatient_total_charges') }}                             as inpatient_total_charges,
        {{ stg_float('outpatient_total_charges') }}                            as outpatient_total_charges,
        {{ stg_float('combined_outpatient_inpatient_total_charges') }}       as combined_outpatient_inpatient_total_charges,

        -- wage-related costs
        {{ stg_float('wage_related_costs_core') }}                            as wage_related_costs_core,
        {{ stg_float('wage_related_costs_rhc_fqhc') }}                        as wage_related_costs_rhc_fqhc,
        {{ stg_float('total_salaries_adjusted') }}                            as total_salaries_adjusted,
        {{ stg_float('contract_labor_direct_patient_care') }}                 as contract_labor_direct_patient_care,
        {{ stg_float('wage_related_costs_for_part_a_teaching_physicians') }} as wage_related_costs_part_a_teaching_physicians,
        {{ stg_float('wage_related_costs_for_interns_and_residents') }}        as wage_related_costs_interns_and_residents,

        -- current assets
        {{ stg_float('cash_on_hand_and_in_banks') }}                           as cash_on_hand_and_in_banks,
        {{ stg_float('temporary_investments') }}                               as temporary_investments,
        {{ stg_float('notes_receivable') }}                                    as notes_receivable,
        {{ stg_float('accounts_receivable') }}                                 as accounts_receivable,
        {{ stg_float('less_allowances_for_uncollectible_notes_and_accounts_receivable') }} as allowances_for_uncollectible_receivables,
        {{ stg_float('inventory') }}                                           as inventory,
        {{ stg_float('prepaid_expenses') }}                                    as prepaid_expenses,
        {{ stg_float('other_current_assets') }}                                as other_current_assets,
        {{ stg_float('total_current_assets') }}                                as total_current_assets,

        -- fixed assets
        {{ stg_float('land') }}                                                as land,
        {{ stg_float('land_improvements') }}                                   as land_improvements,
        {{ stg_float('buildings') }}                                           as buildings,
        {{ stg_float('leasehold_improvements') }}                              as leasehold_improvements,
        {{ stg_float('fixed_equipment') }}                                     as fixed_equipment,
        {{ stg_float('major_movable_equipment') }}                             as major_movable_equipment,
        {{ stg_float('minor_equipment_depreciable') }}                         as minor_equipment_depreciable,
        {{ stg_float('health_information_technology_designated_assets') }}     as health_information_technology_designated_assets,
        {{ stg_float('total_fixed_assets') }}                                  as total_fixed_assets,

        -- other assets
        {{ stg_float('investments') }}                                         as investments,
        {{ stg_float('other_assets') }}                                        as other_assets,
        {{ stg_float('total_other_assets') }}                                  as total_other_assets,
        {{ stg_float('total_assets') }}                                        as total_assets,

        -- current liabilities
        {{ stg_float('accounts_payable') }}                                    as accounts_payable,
        {{ stg_float('salaries_wages_and_fees_payable') }}                   as salaries_wages_and_fees_payable,
        {{ stg_float('payroll_taxes_payable') }}                               as payroll_taxes_payable,
        {{ stg_float('notes_and_loans_payable_short_term') }}                 as notes_and_loans_payable_short_term,
        {{ stg_float('deferred_income') }}                                     as deferred_income,
        {{ stg_float('other_current_liabilities') }}                           as other_current_liabilities,
        {{ stg_float('total_current_liabilities') }}                           as total_current_liabilities,

        -- long-term liabilities
        {{ stg_float('mortgage_payable') }}                                    as mortgage_payable,
        {{ stg_float('notes_payable') }}                                       as notes_payable,
        {{ stg_float('unsecured_loans') }}                                     as unsecured_loans,
        {{ stg_float('other_long_term_liabilities') }}                         as other_long_term_liabilities,
        {{ stg_float('total_long_term_liabilities') }}                         as total_long_term_liabilities,
        {{ stg_float('total_liabilities') }}                                   as total_liabilities,

        -- fund balances
        {{ stg_float('general_fund_balance') }}                                as general_fund_balance,
        {{ stg_float('total_fund_balances') }}                                 as total_fund_balances,
        {{ stg_float('total_liabilities_and_fund_balances') }}                 as total_liabilities_and_fund_balances,

        -- drg / medicare payments
        {{ stg_float('drg_amounts_other_than_outlier_payments') }}             as drg_amounts_other_than_outlier_payments,
        {{ stg_float('drg_amounts_before_october_1') }}                        as drg_amounts_before_october_1,
        {{ stg_float('drg_amounts_after_october_1') }}                         as drg_amounts_after_october_1,
        {{ stg_float('outlier_payments_for_discharges') }}                     as outlier_payments_for_discharges,
        {{ stg_float('disproportionate_share_adjustment') }}                   as disproportionate_share_adjustment,
        {{ stg_float('allowable_dsh_percentage') }}                            as allowable_dsh_percentage,
        {{ stg_float('managed_care_simulated_payments') }}                     as managed_care_simulated_payments,
        {{ stg_float('total_ime_payment') }}                                   as total_ime_payment,

        -- revenue & income
        {{ stg_float('inpatient_revenue') }}                                   as inpatient_revenue,
        {{ stg_float('outpatient_revenue') }}                                  as outpatient_revenue,
        {{ stg_float('total_patient_revenue') }}                               as total_patient_revenue,
        {{ stg_float('less_contractual_allowance_and_discounts_on_patients_accounts') }} as contractual_allowance_and_discounts,
        {{ stg_float('net_patient_revenue') }}                                 as net_patient_revenue,
        {{ stg_float('less_total_operating_expense') }}                        as total_operating_expense,
        {{ stg_float('net_income_from_service_to_patients') }}                 as net_income_from_service_to_patients,
        {{ stg_float('total_other_income') }}                                  as total_other_income,
        {{ stg_float('total_income') }}                                        as total_income,
        {{ stg_float('total_other_expenses') }}                                as total_other_expenses,
        {{ stg_float('net_income') }}                                          as net_income,

        -- ratios
        {{ stg_float('cost_to_charge_ratio') }}                                as cost_to_charge_ratio,

        -- medicaid
        {{ stg_float('net_revenue_from_medicaid') }}                           as net_revenue_from_medicaid,
        {{ stg_float('medicaid_charges') }}                                    as medicaid_charges,
        {{ stg_float('net_revenue_from_stand_alone_chip') }}                   as net_revenue_from_stand_alone_chip,
        {{ stg_float('stand_alone_chip_charges') }}                            as stand_alone_chip_charges,

        -- metadata
        _ingested_at,
        _source_run_id

    from source

),

-- GRAIN, measured 2026-09-06 on all 80,077 rows across 2011-2023:
--   rpt_rec_num is unique. Zero duplicates. It IS the key.
--   provider_ccn + source_file_year is NOT unique -- 1,186 collisions. A
--   hospital can file several short cost-report periods inside one file year,
--   e.g. CCN 340090 in 2014 filed 10/01-01/31, then 02/01-06/30, then 07/01
--   onward. Those splits usually mark an ownership change, which makes them
--   evidence for question E43 rather than noise to collapse.
--
-- The old dedupe partitioned on provider_ccn + hospital_name +
-- fiscal_year_end_date and ordered by _ingested_at. That was safe on one
-- vintage and is not safe now: all thirteen years landed in a single run, so
-- every row carries the same _ingested_at and the tiebreak is arbitrary.
-- Dedupe on the real key instead, which drops nothing.
deduped as (

    select *
    from renamed
    qualify row_number() over (
        partition by rpt_rec_num
        order by _ingested_at desc
    ) = 1

)

select * from deduped
