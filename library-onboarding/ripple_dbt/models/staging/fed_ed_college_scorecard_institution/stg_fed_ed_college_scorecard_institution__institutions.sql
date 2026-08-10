{{ config(materialized='view') }}

-- The College Scorecard institution-level landing table is 3,311 columns wide
-- (every metric x every cohort/demographic slice). This staging model selects
-- a curated core of ~60 columns: identity, location, control/level,
-- admissions, enrollment, costs / net price, completion, earnings, debt, and
-- default/repayment rates. The full width remains in the landing table.

with

source as (

    select * from {{ source('ripple_raw', 'FED_ED_COLLEGE_SCORECARD_INSTITUTION') }}

),

renamed as (

    select

        -- identity
        trim(UNITID)                                   as unitid,
        trim(OPEID)                                    as opeid,
        trim(OPEID6)                                   as opeid6,
        trim(INSTNM)                                   as institution_name,
        trim(INSTURL)                                  as institution_url,
        trim(NPCURL)                                   as net_price_calculator_url,
        trim(ACCREDAGENCY)                             as accrediting_agency,
        try_to_number(trim(MAIN))                      as is_main_campus,
        try_to_number(trim(NUMBRANCH))                 as branch_count,
        try_to_number(trim(CURROPER))                  as currently_operating,

        -- location
        trim(CITY)                                     as city,
        trim(STABBR)                                   as state,
        trim(ZIP)                                      as zip,
        trim(ST_FIPS)                                  as state_fips,
        try_to_number(trim(REGION))                    as region_code,
        try_to_number(trim(LOCALE))                    as locale_code,
        try_to_double(trim(LATITUDE))                  as latitude,
        try_to_double(trim(LONGITUDE))                 as longitude,

        -- control / level / type
        try_to_number(trim(CONTROL))                   as control_code,
        try_to_number(trim(ICLEVEL))                   as institution_level_code,
        try_to_number(trim(PREDDEG))                   as predominant_degree_code,
        try_to_number(trim(HIGHDEG))                   as highest_degree_code,
        try_to_number(trim(CCBASIC))                   as carnegie_basic_code,
        try_to_number(trim(HBCU))                      as is_hbcu,
        try_to_number(trim(PBI))                       as is_pbi,
        try_to_number(trim(TRIBAL))                    as is_tribal,
        try_to_number(trim(HSI))                       as is_hsi,
        try_to_number(trim(MENONLY))                   as is_men_only,
        try_to_number(trim(WOMENONLY))                 as is_women_only,
        try_to_number(trim(RELAFFIL))                  as religious_affiliation_code,
        try_to_number(trim(DISTANCEONLY))              as is_distance_only,

        -- admissions
        try_to_double(trim(ADM_RATE))                  as admission_rate,
        try_to_double(trim(ADM_RATE_ALL))              as admission_rate_all_campuses,
        try_to_number(trim(SAT_AVG))                   as sat_avg,
        try_to_number(trim(ACTCMMID))                  as act_composite_midpoint,

        -- enrollment
        try_to_number(trim(UGDS))                      as undergrad_enrollment,

        -- costs / net price
        try_to_number(trim(NPT4_PUB))                  as net_price_public,
        try_to_number(trim(NPT4_PRIV))                 as net_price_private,
        try_to_number(trim(COSTT4_A))                  as cost_of_attendance_academic_year,
        try_to_number(trim(COSTT4_P))                  as cost_of_attendance_program_year,
        try_to_number(trim(TUITIONFEE_IN))             as tuition_in_state,
        try_to_number(trim(TUITIONFEE_OUT))            as tuition_out_of_state,
        try_to_number(trim(TUITIONFEE_PROG))           as tuition_program_year,
        try_to_number(trim(TUITFTE))                   as tuition_revenue_per_fte,
        try_to_number(trim(INEXPFTE))                  as instructional_spend_per_fte,
        try_to_number(trim(AVGFACSAL))                 as avg_faculty_salary_monthly,
        try_to_double(trim(PFTFAC))                    as pct_full_time_faculty,

        -- aid
        try_to_double(trim(PCTPELL))                   as pct_pell,
        try_to_double(trim(PCTFLOAN))                  as pct_federal_loan,

        -- completion / retention
        try_to_double(trim(C150_4))                    as completion_rate_150pct_4yr,
        try_to_double(trim(C150_L4))                   as completion_rate_150pct_lt4yr,
        try_to_double(trim(RET_FT4))                   as retention_full_time_4yr,
        try_to_double(trim(RET_FTL4))                  as retention_full_time_lt4yr,

        -- debt / default / repayment
        try_to_double(trim(CDR2))                      as default_rate_2yr,
        try_to_double(trim(CDR3))                      as default_rate_3yr,
        try_to_double(trim(RPY_3YR_RT))                as repayment_rate_3yr,
        try_to_number(trim(DEBT_MDN))                  as debt_median,
        try_to_number(trim(GRAD_DEBT_MDN))             as debt_median_completers,
        try_to_number(trim(WDRAW_DEBT_MDN))            as debt_median_withdrawn,

        -- earnings
        try_to_number(trim(MD_EARN_WNE_P6))            as earnings_median_6yr,
        try_to_number(trim(MD_EARN_WNE_P8))            as earnings_median_8yr,
        try_to_number(trim(MD_EARN_WNE_P10))           as earnings_median_10yr,
        try_to_number(trim(MN_EARN_WNE_P10))           as earnings_mean_10yr,

        -- metadata (INGESTED_AT is a NUMBER epoch in microseconds)
        to_timestamp_ntz(INGESTED_AT, 6)               as _loaded_at,
        SOURCE_RUN_ID                                  as _source_run_id,
        SRC_SHA256                                     as _src_sha256

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by unitid
            order by _loaded_at desc
        ) as _row_num
    from renamed
    where unitid is not null

)

select * exclude (_row_num)
from deduped
where _row_num = 1
