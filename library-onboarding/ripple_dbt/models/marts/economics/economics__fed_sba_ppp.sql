{{ config(materialized='table', schema='ECONOMICS') }}

-- GRAIN: one row per loan (LOANNUMBER)
-- Answers: PPP pandemic relief distribution â€” who got how much, where, forgiveness rates
-- Source: SBA Paycheck Protection Program (968K rows)
-- Key joins: BORROWERSTATE/PROJECTSTATE â†’ DIM_STATE, CD â†’ congressional district

with source as (

    select * from {{ source('ripple_raw', 'FED_SBA_PPP') }}

),

cleaned as (

    select
        LOANNUMBER as loan_number,
        try_to_date(DATEAPPROVED) as date_approved,
        PROCESSINGMETHOD as processing_method,
        BORROWERNAME as borrower_name,
        BORROWERCITY as borrower_city,
        BORROWERSTATE as borrower_state,
        BORROWERZIP as borrower_zip,
        LOANSTATUS as loan_status,
        try_to_date(LOANSTATUSDATE) as loan_status_date,
        try_to_number(TERM) as term_months,
        try_to_double(INITIALAPPROVALAMOUNT) as initial_approval_amount,
        try_to_double(CURRENTAPPROVALAMOUNT) as current_approval_amount,
        try_to_double(UNDISBURSEDAMOUNT) as undisbursed_amount,
        SERVICINGLENDERNAME as servicing_lender_name,
        SERVICINGLENDERSTATE as servicing_lender_state,
        RURALURBANINDICATOR as rural_urban_indicator,
        HUBZONEINDICATOR as hubzone_indicator,
        LMIINDICATOR as lmi_indicator,
        BUSINESSAGEDESCRIPTION as business_age,
        PROJECTSTATE as project_state,
        PROJECTCOUNTYNAME as project_county,
        CD as congressional_district,
        try_to_number(JOBSREPORTED) as jobs_reported,
        NAICSCODE as naics_code,
        RACE as race,
        ETHNICITY as ethnicity,
        try_to_double(PAYROLL_PROCEED) as payroll_proceed,
        try_to_double(RENT_PROCEED) as rent_proceed,
        try_to_double(UTILITIES_PROCEED) as utilities_proceed,
        try_to_double(MORTGAGE_INTEREST_PROCEED) as mortgage_interest_proceed

    from source

),

final as (

    select
        *,
        coalesce(payroll_proceed, 0) + coalesce(rent_proceed, 0) 
            + coalesce(utilities_proceed, 0) + coalesce(mortgage_interest_proceed, 0) as total_proceeds_used,
        case when loan_status = 'Paid in Full or Charged Off' then true else false end as is_resolved

    from cleaned
    qualify row_number() over (partition by loan_number order by date_approved desc nulls last,
             -- tie-breakers 2026-09-18: the row's own values, so the same row wins every run
             processing_method nulls last, borrower_name nulls last, borrower_city nulls last,
             borrower_state nulls last, borrower_zip nulls last, loan_status nulls last,
             loan_status_date nulls last, term_months nulls last, initial_approval_amount nulls last,
             current_approval_amount nulls last, undisbursed_amount nulls last,
             servicing_lender_name nulls last, servicing_lender_state nulls last,
             rural_urban_indicator nulls last, hubzone_indicator nulls last, lmi_indicator nulls last,
             business_age nulls last, project_state nulls last, project_county nulls last,
             congressional_district nulls last, jobs_reported nulls last, naics_code nulls last,
             race nulls last, ethnicity nulls last, payroll_proceed nulls last, rent_proceed nulls last,
             utilities_proceed nulls last, mortgage_interest_proceed nulls last
) = 1

)

select * from final
