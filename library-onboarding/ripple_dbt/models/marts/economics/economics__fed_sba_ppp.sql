{{ config(materialized='table', schema='ECONOMICS') }}

-- GRAIN: one row per loan (LOANNUMBER)
-- Answers: PPP pandemic relief distribution â€” who got how much, where, forgiveness rates
-- Source: SBA Paycheck Protection Program (968K rows)
-- Key joins: BORROWERSTATE/PROJECTSTATE â†’ DIM_STATE, CD â†’ congressional district
--
-- KEY RE-PROOF (2026-09-20 -- same hole f41ebff9 closed in staging: 289 views
-- deduped on a key proven unique ONCE, at generation time, that silently stopped
-- identifying a row after a reload while `unique` stayed green forever, because
-- the test only ever checked the ALREADY-DEDUPED output). key_proof below re-runs
-- scripts/generate_staging_models.py's key_is_unique_within_each_load() math live,
-- every build: COUNT(*) vs COUNT(DISTINCT HASH(loan_number)), grouped by
-- _SOURCE_RUN_ID when that column is a genuine load id (>= 100 rows/run average --
-- some CMS tables stamp a per-ROW uuid there instead, which would make ANY key
-- "prove" unique; MIN_ROWS_PER_LOAD=100 mirrors the generator exactly).
-- Live-verified 2026-09-20: 968,524 rows, 968,524 distinct loan_number, 1 load to
-- date, zero collision -- proven, so the QUALIFY below partitions by loan_number
-- alone. If a future reload ever breaks that, would_collapse > 0 and the SAME
-- QUALIFY automatically falls back to a whole-row partition (every data column,
-- so only exact copies collapse) -- schema.yml's `unique` test should be dropped
-- the day this ever shows would_collapse > 0.

with source as (

    select * from {{ source('ripple_raw', 'FED_SBA_PPP') }}

),

key_load_shape as (

    select count(*) as total_rows, count(distinct _SOURCE_RUN_ID) as n_runs
    from source

),

key_proof as (

    select coalesce(sum(n - d), 0) as would_collapse
    from (
        select
            case when ls.n_runs > 0 and ls.total_rows / ls.n_runs >= 100
                 then s._SOURCE_RUN_ID else '__ALL__' end        as _load_id,
            count(*)                                              as n,
            count(distinct hash(s.LOANNUMBER))                    as d
        from source s
        cross join key_load_shape ls
        group by 1
    )

),

cleaned as (

    select
        LOANNUMBER as loan_number,
        {{ stg_date('DATEAPPROVED') }} as date_approved,
        PROCESSINGMETHOD as processing_method,
        BORROWERNAME as borrower_name,
        BORROWERCITY as borrower_city,
        BORROWERSTATE as borrower_state,
        BORROWERZIP as borrower_zip,
        LOANSTATUS as loan_status,
        {{ stg_date('LOANSTATUSDATE') }} as loan_status_date,
        {{ stg_int('TERM') }} as term_months,
        {{ stg_float('INITIALAPPROVALAMOUNT') }} as initial_approval_amount,
        {{ stg_float('CURRENTAPPROVALAMOUNT') }} as current_approval_amount,
        {{ stg_float('UNDISBURSEDAMOUNT') }} as undisbursed_amount,
        SERVICINGLENDERNAME as servicing_lender_name,
        SERVICINGLENDERSTATE as servicing_lender_state,
        RURALURBANINDICATOR as rural_urban_indicator,
        HUBZONEINDICATOR as hubzone_indicator,
        LMIINDICATOR as lmi_indicator,
        BUSINESSAGEDESCRIPTION as business_age,
        PROJECTSTATE as project_state,
        PROJECTCOUNTYNAME as project_county,
        CD as congressional_district,
        {{ stg_int('JOBSREPORTED') }} as jobs_reported,
        NAICSCODE as naics_code,
        RACE as race,
        ETHNICITY as ethnicity,
        {{ stg_float('PAYROLL_PROCEED') }} as payroll_proceed,
        {{ stg_float('RENT_PROCEED') }} as rent_proceed,
        {{ stg_float('UTILITIES_PROCEED') }} as utilities_proceed,
        {{ stg_float('MORTGAGE_INTEREST_PROCEED') }} as mortgage_interest_proceed

    from source

),

final as (

    select
        c.*,
        coalesce(c.payroll_proceed, 0) + coalesce(c.rent_proceed, 0)
            + coalesce(c.utilities_proceed, 0) + coalesce(c.mortgage_interest_proceed, 0) as total_proceeds_used,
        case when c.loan_status = 'Paid in Full or Charged Off' then true else false end as is_resolved

    from cleaned c
    cross join key_proof kp
    -- partition: loan_number is unconditional; every other column only engages
    -- (goes non-null) when kp.would_collapse != 0, i.e. the key is NOT proven --
    -- at that point this IS a whole-row partition (loan_number plus every other
    -- data column), same shape as generate_staging_models.py's fallback.
    qualify row_number() over (partition by
             c.loan_number,
             case when kp.would_collapse != 0 then c.date_approved else null end,
             case when kp.would_collapse != 0 then c.processing_method else null end,
             case when kp.would_collapse != 0 then c.borrower_name else null end,
             case when kp.would_collapse != 0 then c.borrower_city else null end,
             case when kp.would_collapse != 0 then c.borrower_state else null end,
             case when kp.would_collapse != 0 then c.borrower_zip else null end,
             case when kp.would_collapse != 0 then c.loan_status else null end,
             case when kp.would_collapse != 0 then c.loan_status_date else null end,
             case when kp.would_collapse != 0 then c.term_months else null end,
             case when kp.would_collapse != 0 then c.initial_approval_amount else null end,
             case when kp.would_collapse != 0 then c.current_approval_amount else null end,
             case when kp.would_collapse != 0 then c.undisbursed_amount else null end,
             case when kp.would_collapse != 0 then c.servicing_lender_name else null end,
             case when kp.would_collapse != 0 then c.servicing_lender_state else null end,
             case when kp.would_collapse != 0 then c.rural_urban_indicator else null end,
             case when kp.would_collapse != 0 then c.hubzone_indicator else null end,
             case when kp.would_collapse != 0 then c.lmi_indicator else null end,
             case when kp.would_collapse != 0 then c.business_age else null end,
             case when kp.would_collapse != 0 then c.project_state else null end,
             case when kp.would_collapse != 0 then c.project_county else null end,
             case when kp.would_collapse != 0 then c.congressional_district else null end,
             case when kp.would_collapse != 0 then c.jobs_reported else null end,
             case when kp.would_collapse != 0 then c.naics_code else null end,
             case when kp.would_collapse != 0 then c.race else null end,
             case when kp.would_collapse != 0 then c.ethnicity else null end,
             case when kp.would_collapse != 0 then c.payroll_proceed else null end,
             case when kp.would_collapse != 0 then c.rent_proceed else null end,
             case when kp.would_collapse != 0 then c.utilities_proceed else null end,
             case when kp.would_collapse != 0 then c.mortgage_interest_proceed else null end
             order by c.date_approved desc nulls last,
             -- tie-breakers 2026-09-18: the row's own values, so the same row wins every run
             c.processing_method nulls last, c.borrower_name nulls last, c.borrower_city nulls last,
             c.borrower_state nulls last, c.borrower_zip nulls last, c.loan_status nulls last,
             c.loan_status_date nulls last, c.term_months nulls last, c.initial_approval_amount nulls last,
             c.current_approval_amount nulls last, c.undisbursed_amount nulls last,
             c.servicing_lender_name nulls last, c.servicing_lender_state nulls last,
             c.rural_urban_indicator nulls last, c.hubzone_indicator nulls last, c.lmi_indicator nulls last,
             c.business_age nulls last, c.project_state nulls last, c.project_county nulls last,
             c.congressional_district nulls last, c.jobs_reported nulls last, c.naics_code nulls last,
             c.race nulls last, c.ethnicity nulls last, c.payroll_proceed nulls last, c.rent_proceed nulls last,
             c.utilities_proceed nulls last, c.mortgage_interest_proceed nulls last
) = 1

)

select
    loan_number, date_approved, processing_method, borrower_name, borrower_city,
    borrower_state, borrower_zip, loan_status, loan_status_date, term_months,
    initial_approval_amount, current_approval_amount, undisbursed_amount,
    servicing_lender_name, servicing_lender_state, rural_urban_indicator,
    hubzone_indicator, lmi_indicator, business_age, project_state, project_county,
    congressional_district, jobs_reported, naics_code, race, ethnicity,
    payroll_proceed, rent_proceed, utilities_proceed, mortgage_interest_proceed,
    total_proceeds_used, is_resolved
from final
