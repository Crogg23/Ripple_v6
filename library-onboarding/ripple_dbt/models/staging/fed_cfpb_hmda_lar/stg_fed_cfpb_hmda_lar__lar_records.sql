{{ config(materialized='view') }}

-- SAMPLE ONLY: this landing table holds 17,474 rows -- a tiny slice of the
-- multi-million-row national HMDA LAR corpus. Loan-level data with no natural
-- key; LEI + ACTIVITY_YEAR verified NOT unique, so lar_record_id appends a
-- row_number() over the full-row hash as a deterministic tiebreaker.

with

source as (

    select * from {{ source('ripple_raw', 'FED_CFPB_HMDA_LAR') }}

),

keyed as (

    select
        source.*,
        {{ dbt_utils.generate_surrogate_key(['LEI', 'ACTIVITY_YEAR']) }}
            || '-'
            || row_number() over (
                   partition by LEI, ACTIVITY_YEAR
                   order by hash(*)
               ) as lar_record_id
    from source

),

renamed as (

    select

        -- identifiers
        lar_record_id,
        try_to_number(trim(ACTIVITY_YEAR))               as activity_year,
        trim(LEI)                                        as lei,

        -- geography
        trim(DERIVED_MSA_MD)                             as derived_msa_md,
        trim(STATE_CODE)                                 as state_code,
        trim(COUNTY_CODE)                                as county_code,
        trim(CENSUS_TRACT)                               as census_tract,

        -- derived classifications
        trim(CONFORMING_LOAN_LIMIT)                      as conforming_loan_limit,
        trim(DERIVED_LOAN_PRODUCT_TYPE)                  as derived_loan_product_type,
        trim(DERIVED_DWELLING_CATEGORY)                  as derived_dwelling_category,
        trim(DERIVED_ETHNICITY)                          as derived_ethnicity,
        trim(DERIVED_RACE)                               as derived_race,
        trim(DERIVED_SEX)                                as derived_sex,

        -- action / loan coded fields
        trim(ACTION_TAKEN)                               as action_taken,
        trim(PURCHASER_TYPE)                             as purchaser_type,
        trim(PREAPPROVAL)                                as preapproval,
        trim(LOAN_TYPE)                                  as loan_type,
        trim(LOAN_PURPOSE)                               as loan_purpose,
        trim(LIEN_STATUS)                                as lien_status,
        trim(REVERSE_MORTGAGE)                           as reverse_mortgage,
        trim(OPEN_END_LINE_OF_CREDIT)                    as open_end_line_of_credit,
        trim(BUSINESS_OR_COMMERCIAL_PURPOSE)             as business_or_commercial_purpose,

        -- loan economics
        try_to_number(trim(LOAN_AMOUNT), 18, 2)          as loan_amount,
        try_to_number(trim(LOAN_TO_VALUE_RATIO), 18, 5)  as loan_to_value_ratio,
        try_to_number(trim(INTEREST_RATE), 10, 4)        as interest_rate,
        try_to_number(trim(RATE_SPREAD), 10, 4)          as rate_spread,
        trim(HOEPA_STATUS)                               as hoepa_status,
        try_to_number(trim(TOTAL_LOAN_COSTS), 18, 2)     as total_loan_costs,
        try_to_number(trim(TOTAL_POINTS_AND_FEES), 18, 2) as total_points_and_fees,
        try_to_number(trim(ORIGINATION_CHARGES), 18, 2)  as origination_charges,
        try_to_number(trim(DISCOUNT_POINTS), 18, 2)      as discount_points,
        try_to_number(trim(LENDER_CREDITS), 18, 2)       as lender_credits,
        try_to_number(trim(LOAN_TERM))                   as loan_term_months,
        try_to_number(trim(PREPAYMENT_PENALTY_TERM))     as prepayment_penalty_term,
        try_to_number(trim(INTRO_RATE_PERIOD))           as intro_rate_period,

        -- loan features
        trim(NEGATIVE_AMORTIZATION)                      as negative_amortization,
        trim(INTEREST_ONLY_PAYMENT)                      as interest_only_payment,
        trim(BALLOON_PAYMENT)                            as balloon_payment,
        trim(OTHER_NONAMORTIZING_FEATURES)               as other_nonamortizing_features,

        -- property
        try_to_number(trim(PROPERTY_VALUE))              as property_value,
        trim(CONSTRUCTION_METHOD)                        as construction_method,
        trim(OCCUPANCY_TYPE)                             as occupancy_type,
        trim(MANUFACTURED_HOME_SECURED_PROPERTY_TYPE)    as manufactured_home_secured_property_type,
        trim(MANUFACTURED_HOME_LAND_PROPERTY_INTEREST)   as manufactured_home_land_property_interest,
        trim(TOTAL_UNITS)                                as total_units,
        try_to_number(trim(MULTIFAMILY_AFFORDABLE_UNITS)) as multifamily_affordable_units,

        -- applicant financials
        try_to_number(trim(INCOME))                      as income_thousands,
        trim(DEBT_TO_INCOME_RATIO)                       as debt_to_income_ratio,
        trim(APPLICANT_CREDIT_SCORE_TYPE)                as applicant_credit_score_type,
        trim(CO_APPLICANT_CREDIT_SCORE_TYPE)             as co_applicant_credit_score_type,

        -- applicant / co-applicant demographics (coded)
        trim(APPLICANT_ETHNICITY_1)                      as applicant_ethnicity_1,
        trim(APPLICANT_ETHNICITY_2)                      as applicant_ethnicity_2,
        trim(APPLICANT_ETHNICITY_3)                      as applicant_ethnicity_3,
        trim(APPLICANT_ETHNICITY_4)                      as applicant_ethnicity_4,
        trim(APPLICANT_ETHNICITY_5)                      as applicant_ethnicity_5,
        trim(CO_APPLICANT_ETHNICITY_1)                   as co_applicant_ethnicity_1,
        trim(CO_APPLICANT_ETHNICITY_2)                   as co_applicant_ethnicity_2,
        CO_APPLICANT_ETHNICITY_3                         as co_applicant_ethnicity_3,
        CO_APPLICANT_ETHNICITY_4                         as co_applicant_ethnicity_4,
        CO_APPLICANT_ETHNICITY_5                         as co_applicant_ethnicity_5,
        trim(APPLICANT_ETHNICITY_OBSERVED)               as applicant_ethnicity_observed,
        trim(CO_APPLICANT_ETHNICITY_OBSERVED)            as co_applicant_ethnicity_observed,
        trim(APPLICANT_RACE_1)                           as applicant_race_1,
        trim(APPLICANT_RACE_2)                           as applicant_race_2,
        trim(APPLICANT_RACE_3)                           as applicant_race_3,
        trim(APPLICANT_RACE_4)                           as applicant_race_4,
        trim(APPLICANT_RACE_5)                           as applicant_race_5,
        trim(CO_APPLICANT_RACE_1)                        as co_applicant_race_1,
        trim(CO_APPLICANT_RACE_2)                        as co_applicant_race_2,
        trim(CO_APPLICANT_RACE_3)                        as co_applicant_race_3,
        trim(CO_APPLICANT_RACE_4)                        as co_applicant_race_4,
        trim(CO_APPLICANT_RACE_5)                        as co_applicant_race_5,
        trim(APPLICANT_RACE_OBSERVED)                    as applicant_race_observed,
        trim(CO_APPLICANT_RACE_OBSERVED)                 as co_applicant_race_observed,
        trim(APPLICANT_SEX)                              as applicant_sex,
        trim(CO_APPLICANT_SEX)                           as co_applicant_sex,
        trim(APPLICANT_SEX_OBSERVED)                     as applicant_sex_observed,
        trim(CO_APPLICANT_SEX_OBSERVED)                  as co_applicant_sex_observed,
        trim(APPLICANT_AGE)                              as applicant_age,
        trim(CO_APPLICANT_AGE)                           as co_applicant_age,
        trim(APPLICANT_AGE_ABOVE_62)                     as applicant_age_above_62,
        trim(CO_APPLICANT_AGE_ABOVE_62)                  as co_applicant_age_above_62,

        -- application channel / underwriting
        trim(SUBMISSION_OF_APPLICATION)                  as submission_of_application,
        trim(INITIALLY_PAYABLE_TO_INSTITUTION)           as initially_payable_to_institution,
        trim(AUS_1)                                      as aus_1,
        trim(AUS_2)                                      as aus_2,
        trim(AUS_3)                                      as aus_3,
        trim(AUS_4)                                      as aus_4,
        trim(AUS_5)                                      as aus_5,
        trim(DENIAL_REASON_1)                            as denial_reason_1,
        trim(DENIAL_REASON_2)                            as denial_reason_2,
        trim(DENIAL_REASON_3)                            as denial_reason_3,
        trim(DENIAL_REASON_4)                            as denial_reason_4,

        -- tract context
        try_to_number(trim(TRACT_POPULATION))            as tract_population,
        try_to_number(trim(TRACT_MINORITY_POPULATION_PERCENT), 10, 4) as tract_minority_population_percent,
        try_to_number(trim(FFIEC_MSA_MD_MEDIAN_FAMILY_INCOME))        as ffiec_msa_md_median_family_income,
        try_to_number(trim(TRACT_TO_MSA_INCOME_PERCENTAGE), 10, 4)    as tract_to_msa_income_percentage,
        try_to_number(trim(TRACT_OWNER_OCCUPIED_UNITS))  as tract_owner_occupied_units,
        try_to_number(trim(TRACT_ONE_TO_FOUR_FAMILY_HOMES)) as tract_one_to_four_family_homes,
        try_to_number(trim(TRACT_MEDIAN_AGE_OF_HOUSING_UNITS)) as tract_median_age_of_housing_units,

        -- metadata
        to_timestamp_ntz(INGESTED_AT, 6)                 as _ingested_at,
        SOURCE_RUN_ID                                    as _source_run_id,
        SRC_SHA256                                       as _src_sha256

    from keyed

)

select * from renamed
