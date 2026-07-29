{{ config(materialized='table', schema='ECONOMICS') }}

-- GRAIN: one row per loan (implied by LOCATIONID + BORRNAME + APPROVALDATE + GROSSAPPROVAL)
-- Answers: SBA lending patterns, which businesses get approved, where, for how much?
-- Source: SBA 7(a) and 504 loan data (2.2M rows)
-- Key joins: BORRSTATE/PROJECTSTATE â†’ DIM_STATE

with source as (

    select * from {{ source('ripple_raw', 'FED_SBA_LOANS') }}

),

cleaned as (

    select
        PROGRAM as program,
        SUBPROGRAM as subprogram,
        BORRNAME as borrower_name,
        BORRCITY as borrower_city,
        BORRSTATE as borrower_state,
        BORRZIP as borrower_zip,
        PROJECTCOUNTY as project_county,
        PROJECTSTATE as project_state,
        CONGRESSIONALDISTRICT as congressional_district,
        CDC_NAME as cdc_name,
        CDC_STATE as cdc_state,
        THIRDPARTYLENDER_NAME as lender_name,
        THIRDPARTYLENDER_STATE as lender_state,
        try_to_double(THIRDPARTYDOLLARS) as third_party_dollars,
        try_to_double(GROSSAPPROVAL) as gross_approval_amount,
        try_to_date(APPROVALDATE) as approval_date,
        try_to_number(APPROVALFY) as approval_fiscal_year,
        try_to_date(FIRSTDISBURSEMENTDATE) as first_disbursement_date,
        try_to_number(TERMINMONTHS) as term_months,
        NAICSCODE as naics_code,
        NAICSDESCRIPTION as naics_description,
        BUSINESSTYPE as business_type,
        BUSINESSAGE as business_age,
        LOANSTATUS as loan_status,
        try_to_date(PAIDINFULLDATE) as paid_in_full_date,
        try_to_date(CHARGEOFFDATE) as chargeoff_date,
        try_to_double(GROSSCHARGEOFFAMOUNT) as gross_chargeoff_amount,
        try_to_number(JOBSSUPPORTED) as jobs_supported

    from source

),

final as (

    select
        *,
        case
            when loan_status = 'CHGOFF' then true
            when loan_status = 'PIF' then false
            else null
        end as is_defaulted,
        case
            when gross_chargeoff_amount > 0 and gross_approval_amount > 0
            then round(gross_chargeoff_amount / gross_approval_amount, 4)
        end as loss_rate

    from cleaned

)

select * from final
