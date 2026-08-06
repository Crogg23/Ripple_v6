{{ config(tags=['minimal_staging']) }}

-- GRAIN: NOT YET DETERMINED (one row per LAR record within a SOURCE_YEAR) -- needs manual review.
-- This is a passthrough staging view: snake_case rename only, no dedup.
-- Legacy Respondent ID (respondent_id) is the join key for this era -- NOT lei
-- (that's the modern/2018+ FED_CFPB_HMDA table's key). See schema.yml for context.

with source as (

    select * from {{ source('ripple_raw', 'FED_CFPB_HMDA_HISTORIC') }}

),

renamed as (

    select
        AS_OF_YEAR as as_of_year,
        SOURCE_YEAR as source_year,
        RESPONDENT_ID as respondent_id,
        AGENCY_NAME as agency_name,
        AGENCY_ABBR as agency_abbr,
        AGENCY_CODE as agency_code,
        LOAN_TYPE_NAME as loan_type_name,
        LOAN_TYPE as loan_type,
        PROPERTY_TYPE_NAME as property_type_name,
        PROPERTY_TYPE as property_type,
        LOAN_PURPOSE_NAME as loan_purpose_name,
        LOAN_PURPOSE as loan_purpose,
        OWNER_OCCUPANCY_NAME as owner_occupancy_name,
        OWNER_OCCUPANCY as owner_occupancy,
        LOAN_AMOUNT_000S as loan_amount_000s,
        PREAPPROVAL_NAME as preapproval_name,
        PREAPPROVAL as preapproval,
        ACTION_TAKEN_NAME as action_taken_name,
        ACTION_TAKEN as action_taken,
        MSAMD_NAME as msamd_name,
        MSAMD as msamd,
        STATE_NAME as state_name,
        STATE_ABBR as state_abbr,
        STATE_CODE as state_code,
        COUNTY_NAME as county_name,
        COUNTY_CODE as county_code,
        CENSUS_TRACT_NUMBER as census_tract_number,
        APPLICANT_ETHNICITY_NAME as applicant_ethnicity_name,
        APPLICANT_ETHNICITY as applicant_ethnicity,
        CO_APPLICANT_ETHNICITY_NAME as co_applicant_ethnicity_name,
        CO_APPLICANT_ETHNICITY as co_applicant_ethnicity,
        APPLICANT_RACE_NAME_1 as applicant_race_name_1,
        APPLICANT_RACE_1 as applicant_race_1,
        APPLICANT_RACE_NAME_2 as applicant_race_name_2,
        APPLICANT_RACE_2 as applicant_race_2,
        APPLICANT_RACE_NAME_3 as applicant_race_name_3,
        APPLICANT_RACE_3 as applicant_race_3,
        APPLICANT_RACE_NAME_4 as applicant_race_name_4,
        APPLICANT_RACE_4 as applicant_race_4,
        APPLICANT_RACE_NAME_5 as applicant_race_name_5,
        APPLICANT_RACE_5 as applicant_race_5,
        CO_APPLICANT_RACE_NAME_1 as co_applicant_race_name_1,
        CO_APPLICANT_RACE_1 as co_applicant_race_1,
        CO_APPLICANT_RACE_NAME_2 as co_applicant_race_name_2,
        CO_APPLICANT_RACE_2 as co_applicant_race_2,
        CO_APPLICANT_RACE_NAME_3 as co_applicant_race_name_3,
        CO_APPLICANT_RACE_3 as co_applicant_race_3,
        CO_APPLICANT_RACE_NAME_4 as co_applicant_race_name_4,
        CO_APPLICANT_RACE_4 as co_applicant_race_4,
        CO_APPLICANT_RACE_NAME_5 as co_applicant_race_name_5,
        CO_APPLICANT_RACE_5 as co_applicant_race_5,
        APPLICANT_SEX_NAME as applicant_sex_name,
        APPLICANT_SEX as applicant_sex,
        CO_APPLICANT_SEX_NAME as co_applicant_sex_name,
        CO_APPLICANT_SEX as co_applicant_sex,
        APPLICANT_INCOME_000S as applicant_income_000s,
        PURCHASER_TYPE_NAME as purchaser_type_name,
        PURCHASER_TYPE as purchaser_type,
        DENIAL_REASON_NAME_1 as denial_reason_name_1,
        DENIAL_REASON_1 as denial_reason_1,
        DENIAL_REASON_NAME_2 as denial_reason_name_2,
        DENIAL_REASON_2 as denial_reason_2,
        DENIAL_REASON_NAME_3 as denial_reason_name_3,
        DENIAL_REASON_3 as denial_reason_3,
        RATE_SPREAD as rate_spread,
        HOEPA_STATUS_NAME as hoepa_status_name,
        HOEPA_STATUS as hoepa_status,
        LIEN_STATUS_NAME as lien_status_name,
        LIEN_STATUS as lien_status,
        EDIT_STATUS_NAME as edit_status_name,
        EDIT_STATUS as edit_status,
        SEQUENCE_NUMBER as sequence_number,
        POPULATION as population,
        MINORITY_POPULATION as minority_population,
        HUD_MEDIAN_FAMILY_INCOME as hud_median_family_income,
        TRACT_TO_MSAMD_INCOME as tract_to_msamd_income,
        NUMBER_OF_OWNER_OCCUPIED_UNITS as number_of_owner_occupied_units,
        NUMBER_OF_1_TO_4_FAMILY_UNITS as number_of_1_to_4_family_units,
        APPLICATION_DATE_INDICATOR as application_date_indicator,
        "_INGESTED_AT" as _loaded_at,
        'https://www.consumerfinance.gov/data-research/hmda/historic-data/' as _source_url

    from source

)

select * from renamed
