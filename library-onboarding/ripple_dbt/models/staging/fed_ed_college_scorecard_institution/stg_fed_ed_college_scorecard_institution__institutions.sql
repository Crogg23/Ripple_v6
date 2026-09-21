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
        {{ stg_int('trim(MAIN)') }}                      as is_main_campus,
        {{ stg_int('trim(NUMBRANCH)') }}                 as branch_count,
        {{ stg_int('trim(CURROPER)') }}                  as currently_operating,

        -- location
        trim(CITY)                                     as city,
        trim(STABBR)                                   as state,
        trim(ZIP)                                      as zip,
        trim(ST_FIPS)                                  as state_fips,
        {{ stg_int('trim(REGION)') }}                    as region_code,
        {{ stg_int('trim(LOCALE)') }}                    as locale_code,
        {{ stg_float('trim(LATITUDE)') }}                  as latitude,
        {{ stg_float('trim(LONGITUDE)') }}                 as longitude,

        -- control / level / type
        {{ stg_int('trim(CONTROL)') }}                   as control_code,
        {{ stg_int('trim(ICLEVEL)') }}                   as institution_level_code,
        {{ stg_int('trim(PREDDEG)') }}                   as predominant_degree_code,
        {{ stg_int('trim(HIGHDEG)') }}                   as highest_degree_code,
        {{ stg_int('trim(CCBASIC)') }}                   as carnegie_basic_code,
        {{ stg_int('trim(HBCU)') }}                      as is_hbcu,
        {{ stg_int('trim(PBI)') }}                       as is_pbi,
        {{ stg_int('trim(TRIBAL)') }}                    as is_tribal,
        {{ stg_int('trim(HSI)') }}                       as is_hsi,
        {{ stg_int('trim(MENONLY)') }}                   as is_men_only,
        {{ stg_int('trim(WOMENONLY)') }}                 as is_women_only,
        {{ stg_int('trim(RELAFFIL)') }}                  as religious_affiliation_code,
        {{ stg_int('trim(DISTANCEONLY)') }}              as is_distance_only,

        -- admissions
        {{ stg_float('trim(ADM_RATE)') }}                  as admission_rate,
        {{ stg_float('trim(ADM_RATE_ALL)') }}              as admission_rate_all_campuses,
        {{ stg_int('trim(SAT_AVG)') }}                   as sat_avg,
        {{ stg_int('trim(ACTCMMID)') }}                  as act_composite_midpoint,

        -- enrollment
        {{ stg_int('trim(UGDS)') }}                      as undergrad_enrollment,

        -- costs / net price
        {{ stg_int('trim(NPT4_PUB)') }}                  as net_price_public,
        {{ stg_int('trim(NPT4_PRIV)') }}                 as net_price_private,
        {{ stg_int('trim(COSTT4_A)') }}                  as cost_of_attendance_academic_year,
        {{ stg_int('trim(COSTT4_P)') }}                  as cost_of_attendance_program_year,
        {{ stg_int('trim(TUITIONFEE_IN)') }}             as tuition_in_state,
        {{ stg_int('trim(TUITIONFEE_OUT)') }}            as tuition_out_of_state,
        {{ stg_int('trim(TUITIONFEE_PROG)') }}           as tuition_program_year,
        {{ stg_int('trim(TUITFTE)') }}                   as tuition_revenue_per_fte,
        {{ stg_int('trim(INEXPFTE)') }}                  as instructional_spend_per_fte,
        {{ stg_int('trim(AVGFACSAL)') }}                 as avg_faculty_salary_monthly,
        {{ stg_float('trim(PFTFAC)') }}                    as pct_full_time_faculty,

        -- aid
        {{ stg_float('trim(PCTPELL)') }}                   as pct_pell,
        {{ stg_float('trim(PCTFLOAN)') }}                  as pct_federal_loan,

        -- completion / retention
        {{ stg_float('trim(C150_4)') }}                    as completion_rate_150pct_4yr,
        {{ stg_float('trim(C150_L4)') }}                   as completion_rate_150pct_lt4yr,
        {{ stg_float('trim(RET_FT4)') }}                   as retention_full_time_4yr,
        {{ stg_float('trim(RET_FTL4)') }}                  as retention_full_time_lt4yr,

        -- debt / default / repayment
        {{ stg_float('trim(CDR2)') }}                      as default_rate_2yr,
        {{ stg_float('trim(CDR3)') }}                      as default_rate_3yr,
        {{ stg_float('trim(RPY_3YR_RT)') }}                as repayment_rate_3yr,
        {{ stg_int('trim(DEBT_MDN)') }}                  as debt_median,
        {{ stg_int('trim(GRAD_DEBT_MDN)') }}             as debt_median_completers,
        {{ stg_int('trim(WDRAW_DEBT_MDN)') }}            as debt_median_withdrawn,

        -- earnings
        {{ stg_int('trim(MD_EARN_WNE_P6)') }}            as earnings_median_6yr,
        {{ stg_int('trim(MD_EARN_WNE_P8)') }}            as earnings_median_8yr,
        {{ stg_int('trim(MD_EARN_WNE_P10)') }}           as earnings_median_10yr,
        {{ stg_int('trim(MN_EARN_WNE_P10)') }}           as earnings_mean_10yr,

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
