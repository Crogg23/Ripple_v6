{{ config(materialized='view') }}

-- GRAIN: one row = one anonymized HMDA LAR loan-application record (2015-2017 only).
-- No natural key exists in the pre-2018 LAR files; lar_record_id is a surrogate
-- (md5 over all business columns + a row_number tiebreaker). Identical rows are
-- LEGITIMATE distinct applications in LAR files -- the tiebreaker keeps them apart.
-- Legacy Respondent ID (respondent_id) is the lender join key for this era -- NOT lei
-- (that's the modern/2018+ FED_CFPB_HMDA table's key).
-- Coverage: AS_OF_YEAR 2015-2017 ONLY (verified) -- "historic" means the pre-2018
-- LAR file format; only 2015, 2016, and 2017 are landed.

with source as (

    select * from {{ source('ripple_raw', 'FED_CFPB_HMDA_HISTORIC') }}

),

renamed as (

    select

        -- filing identity
        trim(AS_OF_YEAR)                                as as_of_year,
        trim(SOURCE_YEAR)                               as source_year,
        trim(RESPONDENT_ID)                             as respondent_id,
        trim(AGENCY_NAME)                               as agency_name,
        trim(AGENCY_ABBR)                               as agency_abbr,
        trim(AGENCY_CODE)                               as agency_code,
        trim(SEQUENCE_NUMBER)                           as sequence_number,

        -- loan attributes (codes kept as text)
        trim(LOAN_TYPE_NAME)                            as loan_type_name,
        trim(LOAN_TYPE)                                 as loan_type,
        trim(PROPERTY_TYPE_NAME)                        as property_type_name,
        trim(PROPERTY_TYPE)                             as property_type,
        trim(LOAN_PURPOSE_NAME)                         as loan_purpose_name,
        trim(LOAN_PURPOSE)                              as loan_purpose,
        trim(OWNER_OCCUPANCY_NAME)                      as owner_occupancy_name,
        trim(OWNER_OCCUPANCY)                           as owner_occupancy,
        try_to_number(trim(LOAN_AMOUNT_000S))           as loan_amount_000s,
        trim(PREAPPROVAL_NAME)                          as preapproval_name,
        trim(PREAPPROVAL)                               as preapproval,
        trim(ACTION_TAKEN_NAME)                         as action_taken_name,
        trim(ACTION_TAKEN)                              as action_taken,

        -- geography
        trim(MSAMD_NAME)                                as msamd_name,
        trim(MSAMD)                                     as msamd,
        trim(STATE_NAME)                                as state_name,
        trim(STATE_ABBR)                                as state_abbr,
        trim(STATE_CODE)                                as state_code,
        trim(COUNTY_NAME)                               as county_name,
        trim(COUNTY_CODE)                               as county_code,
        trim(CENSUS_TRACT_NUMBER)                       as census_tract_number,

        -- applicant demographics (codes kept as text)
        trim(APPLICANT_ETHNICITY_NAME)                  as applicant_ethnicity_name,
        trim(APPLICANT_ETHNICITY)                       as applicant_ethnicity,
        trim(CO_APPLICANT_ETHNICITY_NAME)               as co_applicant_ethnicity_name,
        trim(CO_APPLICANT_ETHNICITY)                    as co_applicant_ethnicity,
        trim(APPLICANT_RACE_NAME_1)                     as applicant_race_name_1,
        trim(APPLICANT_RACE_1)                          as applicant_race_1,
        trim(APPLICANT_RACE_NAME_2)                     as applicant_race_name_2,
        trim(APPLICANT_RACE_2)                          as applicant_race_2,
        trim(APPLICANT_RACE_NAME_3)                     as applicant_race_name_3,
        trim(APPLICANT_RACE_3)                          as applicant_race_3,
        trim(APPLICANT_RACE_NAME_4)                     as applicant_race_name_4,
        trim(APPLICANT_RACE_4)                          as applicant_race_4,
        trim(APPLICANT_RACE_NAME_5)                     as applicant_race_name_5,
        trim(APPLICANT_RACE_5)                          as applicant_race_5,
        trim(CO_APPLICANT_RACE_NAME_1)                  as co_applicant_race_name_1,
        trim(CO_APPLICANT_RACE_1)                       as co_applicant_race_1,
        trim(CO_APPLICANT_RACE_NAME_2)                  as co_applicant_race_name_2,
        trim(CO_APPLICANT_RACE_2)                       as co_applicant_race_2,
        trim(CO_APPLICANT_RACE_NAME_3)                  as co_applicant_race_name_3,
        trim(CO_APPLICANT_RACE_3)                       as co_applicant_race_3,
        trim(CO_APPLICANT_RACE_NAME_4)                  as co_applicant_race_name_4,
        trim(CO_APPLICANT_RACE_4)                       as co_applicant_race_4,
        trim(CO_APPLICANT_RACE_NAME_5)                  as co_applicant_race_name_5,
        trim(CO_APPLICANT_RACE_5)                       as co_applicant_race_5,
        trim(APPLICANT_SEX_NAME)                        as applicant_sex_name,
        trim(APPLICANT_SEX)                             as applicant_sex,
        trim(CO_APPLICANT_SEX_NAME)                     as co_applicant_sex_name,
        trim(CO_APPLICANT_SEX)                          as co_applicant_sex,
        try_to_number(trim(APPLICANT_INCOME_000S))      as applicant_income_000s,

        -- outcome / pricing
        trim(PURCHASER_TYPE_NAME)                       as purchaser_type_name,
        trim(PURCHASER_TYPE)                            as purchaser_type,
        cast(DENIAL_REASON_NAME_1 as varchar)           as denial_reason_name_1,
        cast(DENIAL_REASON_1 as varchar)                as denial_reason_1,
        cast(DENIAL_REASON_NAME_2 as varchar)           as denial_reason_name_2,
        cast(DENIAL_REASON_2 as varchar)                as denial_reason_2,
        cast(DENIAL_REASON_NAME_3 as varchar)           as denial_reason_name_3,
        cast(DENIAL_REASON_3 as varchar)                as denial_reason_3,
        try_to_number(trim(RATE_SPREAD))                as rate_spread,
        trim(HOEPA_STATUS_NAME)                         as hoepa_status_name,
        trim(HOEPA_STATUS)                              as hoepa_status,
        trim(LIEN_STATUS_NAME)                          as lien_status_name,
        trim(LIEN_STATUS)                               as lien_status,
        trim(EDIT_STATUS_NAME)                          as edit_status_name,
        trim(EDIT_STATUS)                               as edit_status,

        -- census-tract context
        try_to_number(trim(POPULATION))                 as population,
        try_to_number(trim(MINORITY_POPULATION))        as minority_population,
        try_to_number(trim(HUD_MEDIAN_FAMILY_INCOME))   as hud_median_family_income,
        try_to_number(trim(TRACT_TO_MSAMD_INCOME))      as tract_to_msamd_income,
        try_to_number(trim(NUMBER_OF_OWNER_OCCUPIED_UNITS)) as number_of_owner_occupied_units,
        try_to_number(trim(NUMBER_OF_1_TO_4_FAMILY_UNITS))  as number_of_1_to_4_family_units,
        trim(APPLICATION_DATE_INDICATOR)                as application_date_indicator,

        -- metadata
        _ingested_at,
        _source_run_id

    from source

),

hashed as (

    select *,
        md5(
            coalesce(as_of_year, '')                                 || '||' ||
            coalesce(source_year, '')                                || '||' ||
            coalesce(respondent_id, '')                              || '||' ||
            coalesce(agency_name, '')                                || '||' ||
            coalesce(agency_abbr, '')                                || '||' ||
            coalesce(agency_code, '')                                || '||' ||
            coalesce(sequence_number, '')                            || '||' ||
            coalesce(loan_type_name, '')                             || '||' ||
            coalesce(loan_type, '')                                  || '||' ||
            coalesce(property_type_name, '')                         || '||' ||
            coalesce(property_type, '')                              || '||' ||
            coalesce(loan_purpose_name, '')                          || '||' ||
            coalesce(loan_purpose, '')                               || '||' ||
            coalesce(owner_occupancy_name, '')                       || '||' ||
            coalesce(owner_occupancy, '')                            || '||' ||
            coalesce(cast(loan_amount_000s as varchar), '')          || '||' ||
            coalesce(preapproval_name, '')                           || '||' ||
            coalesce(preapproval, '')                                || '||' ||
            coalesce(action_taken_name, '')                          || '||' ||
            coalesce(action_taken, '')                               || '||' ||
            coalesce(msamd_name, '')                                 || '||' ||
            coalesce(msamd, '')                                      || '||' ||
            coalesce(state_name, '')                                 || '||' ||
            coalesce(state_abbr, '')                                 || '||' ||
            coalesce(state_code, '')                                 || '||' ||
            coalesce(county_name, '')                                || '||' ||
            coalesce(county_code, '')                                || '||' ||
            coalesce(census_tract_number, '')                        || '||' ||
            coalesce(applicant_ethnicity_name, '')                   || '||' ||
            coalesce(applicant_ethnicity, '')                        || '||' ||
            coalesce(co_applicant_ethnicity_name, '')                || '||' ||
            coalesce(co_applicant_ethnicity, '')                     || '||' ||
            coalesce(applicant_race_name_1, '')                      || '||' ||
            coalesce(applicant_race_1, '')                           || '||' ||
            coalesce(applicant_race_name_2, '')                      || '||' ||
            coalesce(applicant_race_2, '')                           || '||' ||
            coalesce(applicant_race_name_3, '')                      || '||' ||
            coalesce(applicant_race_3, '')                           || '||' ||
            coalesce(applicant_race_name_4, '')                      || '||' ||
            coalesce(applicant_race_4, '')                           || '||' ||
            coalesce(applicant_race_name_5, '')                      || '||' ||
            coalesce(applicant_race_5, '')                           || '||' ||
            coalesce(co_applicant_race_name_1, '')                   || '||' ||
            coalesce(co_applicant_race_1, '')                        || '||' ||
            coalesce(co_applicant_race_name_2, '')                   || '||' ||
            coalesce(co_applicant_race_2, '')                        || '||' ||
            coalesce(co_applicant_race_name_3, '')                   || '||' ||
            coalesce(co_applicant_race_3, '')                        || '||' ||
            coalesce(co_applicant_race_name_4, '')                   || '||' ||
            coalesce(co_applicant_race_4, '')                        || '||' ||
            coalesce(co_applicant_race_name_5, '')                   || '||' ||
            coalesce(co_applicant_race_5, '')                        || '||' ||
            coalesce(applicant_sex_name, '')                         || '||' ||
            coalesce(applicant_sex, '')                              || '||' ||
            coalesce(co_applicant_sex_name, '')                      || '||' ||
            coalesce(co_applicant_sex, '')                           || '||' ||
            coalesce(cast(applicant_income_000s as varchar), '')     || '||' ||
            coalesce(purchaser_type_name, '')                        || '||' ||
            coalesce(purchaser_type, '')                             || '||' ||
            coalesce(denial_reason_name_1, '')                       || '||' ||
            coalesce(denial_reason_1, '')                            || '||' ||
            coalesce(denial_reason_name_2, '')                       || '||' ||
            coalesce(denial_reason_2, '')                            || '||' ||
            coalesce(denial_reason_name_3, '')                       || '||' ||
            coalesce(denial_reason_3, '')                            || '||' ||
            coalesce(cast(rate_spread as varchar), '')               || '||' ||
            coalesce(hoepa_status_name, '')                          || '||' ||
            coalesce(hoepa_status, '')                               || '||' ||
            coalesce(lien_status_name, '')                           || '||' ||
            coalesce(lien_status, '')                                || '||' ||
            coalesce(edit_status_name, '')                           || '||' ||
            coalesce(edit_status, '')                                || '||' ||
            coalesce(cast(population as varchar), '')                || '||' ||
            coalesce(cast(minority_population as varchar), '')       || '||' ||
            coalesce(cast(hud_median_family_income as varchar), '')  || '||' ||
            coalesce(cast(tract_to_msamd_income as varchar), '')     || '||' ||
            coalesce(cast(number_of_owner_occupied_units as varchar), '') || '||' ||
            coalesce(cast(number_of_1_to_4_family_units as varchar), '')  || '||' ||
            coalesce(application_date_indicator, '')
        ) as _record_hash
    from renamed

),

keyed as (

    select *,
        _record_hash || '-' || row_number() over (
            partition by _record_hash
            order by 1
        ) as lar_record_id
    from hashed

)

select * exclude (_record_hash)
from keyed
