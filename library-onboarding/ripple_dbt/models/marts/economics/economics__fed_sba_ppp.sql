{{ config(materialized='table') }}

-- GRAIN: one row per loan (LOANNUMBER)
-- Answers: PPP pandemic relief distribution — who got how much, where, forgiveness rates
-- Source: SBA Paycheck Protection Program (968K rows)
-- Key joins: BORROWERSTATE/PROJECTSTATE → DIM_STATE, CD → congressional district

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
    qualify row_number() over (partition by loan_number order by date_approved desc nulls last) = 1

)

select * from final
