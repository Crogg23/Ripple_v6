{{ config(materialized='view', schema='ECONOMICS') }}

-- GRAIN: one row per federal assistance award transaction
--
-- MATERIALIZED AS A VIEW, not a table (switched 2026-08-22): straight passthrough of a
-- 19.9M-row landing table with guarded casts only -- same call as its contracts twin,
-- which documents the rationale. If a real transform lands here later, switch it back.
--
-- TYPED 2026-08-22: this model had all 112 columns as TEXT -- every obligation amount,
-- outlay, loan face value, and the action date -- while its contracts twin had the
-- identically-named columns cast. Value-checked against the landing table before casting:
-- every money and date column is either 100% castable or the only non-castable value is
-- the empty string (verified by group-by sample), so try_to_double/try_to_date lose
-- nothing real. ZIP, FIPS, and code columns stay TEXT on purpose -- casting strips
-- leading zeros (the 2026-08-10 repair).

with source as (
    select * from {{ source('ripple_raw', 'FED_USASPENDING_ASSISTANCE_FULL') }}
)

select
    "assistance_transaction_unique_key" as ASSISTANCE_TRANSACTION_UNIQUE_KEY,
    "assistance_award_unique_key" as ASSISTANCE_AWARD_UNIQUE_KEY,
    "award_id_fain" as AWARD_ID_FAIN,
    "modification_number" as MODIFICATION_NUMBER,
    "award_id_uri" as AWARD_ID_URI,
    "sai_number" as SAI_NUMBER,
    try_to_double("federal_action_obligation") as FEDERAL_ACTION_OBLIGATION,
    try_to_double("total_obligated_amount") as TOTAL_OBLIGATED_AMOUNT,
    try_to_double("total_outlayed_amount_for_overall_award") as TOTAL_OUTLAYED_AMOUNT_FOR_OVERALL_AWARD,
    try_to_double("indirect_cost_federal_share_amount") as INDIRECT_COST_FEDERAL_SHARE_AMOUNT,
    try_to_double("non_federal_funding_amount") as NON_FEDERAL_FUNDING_AMOUNT,
    try_to_double("total_non_federal_funding_amount") as TOTAL_NON_FEDERAL_FUNDING_AMOUNT,
    try_to_double("face_value_of_loan") as FACE_VALUE_OF_LOAN,
    try_to_double("original_loan_subsidy_cost") as ORIGINAL_LOAN_SUBSIDY_COST,
    try_to_double("total_face_value_of_loan") as TOTAL_FACE_VALUE_OF_LOAN,
    try_to_double("total_loan_subsidy_cost") as TOTAL_LOAN_SUBSIDY_COST,
    try_to_double("generated_pragmatic_obligations") as GENERATED_PRAGMATIC_OBLIGATIONS,
    "disaster_emergency_fund_codes_for_overall_award" as DISASTER_EMERGENCY_FUND_CODES_FOR_OVERALL_AWARD,
    try_to_double("outlayed_amount_from_COVID-19_supplementals_for_overall_award") as OUTLAYED_AMOUNT_FROM_COVID_19_SUPPLEMENTALS_FOR_OVERALL_AWARD,
    try_to_double("obligated_amount_from_COVID-19_supplementals_for_overall_award") as OBLIGATED_AMOUNT_FROM_COVID_19_SUPPLEMENTALS_FOR_OVERALL_AWARD,
    try_to_double("outlayed_amount_from_IIJA_supplemental_for_overall_award") as OUTLAYED_AMOUNT_FROM_IIJA_SUPPLEMENTAL_FOR_OVERALL_AWARD,
    try_to_double("obligated_amount_from_IIJA_supplemental_for_overall_award") as OBLIGATED_AMOUNT_FROM_IIJA_SUPPLEMENTAL_FOR_OVERALL_AWARD,
    try_to_date("action_date") as ACTION_DATE,
    -- fiscal-YEAR number, not a date (same trap fixed on the contracts twin 2026-08-18)
    try_to_number("action_date_fiscal_year") as ACTION_DATE_FISCAL_YEAR,
    -- SENTINEL NULLED 2026-08-20 (time-index scan): USAspending writes 0001-01-01
    -- to mean "no date on file" -- 56,205 rows on the start date and 56,211 on the
    -- current-end date. Left alone it drags any earliest-date reading to the year 1.
    -- nullif runs BEFORE the cast so the sentinel never becomes a year-1 date.
    -- RANGE GUARD 2026-08-22: beyond the exact sentinel, a handful of source typos
    -- survive (years 5, 11, 207, 1008, 3008) plus 9999-09-30 meaning "no end date" --
    -- 14 rows on start, 35 on end, out of 19.9M. Nulled outside 1950-2100 so a single
    -- typo can't drag min/max readings a millennium off.
    case when try_to_date(nullif("period_of_performance_start_date", '0001-01-01'))
              between '1950-01-01' and '2100-01-01'
         then try_to_date(nullif("period_of_performance_start_date", '0001-01-01')) end
        as PERIOD_OF_PERFORMANCE_START_DATE,
    case when try_to_date(nullif("period_of_performance_current_end_date", '0001-01-01'))
              between '1950-01-01' and '2100-01-01'
         then try_to_date(nullif("period_of_performance_current_end_date", '0001-01-01')) end
        as PERIOD_OF_PERFORMANCE_CURRENT_END_DATE,
    "awarding_agency_code" as AWARDING_AGENCY_CODE,
    "awarding_agency_name" as AWARDING_AGENCY_NAME,
    "awarding_sub_agency_code" as AWARDING_SUB_AGENCY_CODE,
    "awarding_sub_agency_name" as AWARDING_SUB_AGENCY_NAME,
    "awarding_office_code" as AWARDING_OFFICE_CODE,
    "awarding_office_name" as AWARDING_OFFICE_NAME,
    "funding_agency_code" as FUNDING_AGENCY_CODE,
    "funding_agency_name" as FUNDING_AGENCY_NAME,
    "funding_sub_agency_code" as FUNDING_SUB_AGENCY_CODE,
    "funding_sub_agency_name" as FUNDING_SUB_AGENCY_NAME,
    "funding_office_code" as FUNDING_OFFICE_CODE,
    "funding_office_name" as FUNDING_OFFICE_NAME,
    "treasury_accounts_funding_this_award" as TREASURY_ACCOUNTS_FUNDING_THIS_AWARD,
    "federal_accounts_funding_this_award" as FEDERAL_ACCOUNTS_FUNDING_THIS_AWARD,
    "object_classes_funding_this_award" as OBJECT_CLASSES_FUNDING_THIS_AWARD,
    "program_activities_funding_this_award" as PROGRAM_ACTIVITIES_FUNDING_THIS_AWARD,
    "recipient_uei" as RECIPIENT_UEI,
    "recipient_duns" as RECIPIENT_DUNS,
    "recipient_name" as RECIPIENT_NAME,
    "recipient_name_raw" as RECIPIENT_NAME_RAW,
    "recipient_parent_uei" as RECIPIENT_PARENT_UEI,
    "recipient_parent_duns" as RECIPIENT_PARENT_DUNS,
    "recipient_parent_name" as RECIPIENT_PARENT_NAME,
    "recipient_parent_name_raw" as RECIPIENT_PARENT_NAME_RAW,
    "recipient_country_code" as RECIPIENT_COUNTRY_CODE,
    "recipient_country_name" as RECIPIENT_COUNTRY_NAME,
    "recipient_address_line_1" as RECIPIENT_ADDRESS_LINE_1,
    "recipient_address_line_2" as RECIPIENT_ADDRESS_LINE_2,
    "recipient_city_code" as RECIPIENT_CITY_CODE,
    "recipient_city_name" as RECIPIENT_CITY_NAME,
    "prime_award_transaction_recipient_county_fips_code" as PRIME_AWARD_TRANSACTION_RECIPIENT_COUNTY_FIPS_CODE,
    "recipient_county_name" as RECIPIENT_COUNTY_NAME,
    "prime_award_transaction_recipient_state_fips_code" as PRIME_AWARD_TRANSACTION_RECIPIENT_STATE_FIPS_CODE,
    "recipient_state_code" as RECIPIENT_STATE_CODE,
    "recipient_state_name" as RECIPIENT_STATE_NAME,
    "recipient_zip_code" as RECIPIENT_ZIP_CODE,
    "recipient_zip_last_4_code" as RECIPIENT_ZIP_LAST_4_CODE,
    "prime_award_transaction_recipient_cd_original" as PRIME_AWARD_TRANSACTION_RECIPIENT_CD_ORIGINAL,
    "prime_award_transaction_recipient_cd_current" as PRIME_AWARD_TRANSACTION_RECIPIENT_CD_CURRENT,
    "recipient_foreign_city_name" as RECIPIENT_FOREIGN_CITY_NAME,
    "recipient_foreign_province_name" as RECIPIENT_FOREIGN_PROVINCE_NAME,
    "recipient_foreign_postal_code" as RECIPIENT_FOREIGN_POSTAL_CODE,
    "primary_place_of_performance_scope" as PRIMARY_PLACE_OF_PERFORMANCE_SCOPE,
    "primary_place_of_performance_country_code" as PRIMARY_PLACE_OF_PERFORMANCE_COUNTRY_CODE,
    "primary_place_of_performance_country_name" as PRIMARY_PLACE_OF_PERFORMANCE_COUNTRY_NAME,
    "primary_place_of_performance_code" as PRIMARY_PLACE_OF_PERFORMANCE_CODE,
    "primary_place_of_performance_city_name" as PRIMARY_PLACE_OF_PERFORMANCE_CITY_NAME,
    "prime_award_transaction_place_of_performance_county_fips_code" as PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE,
    "primary_place_of_performance_county_name" as PRIMARY_PLACE_OF_PERFORMANCE_COUNTY_NAME,
    "prime_award_transaction_place_of_performance_state_fips_code" as PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_STATE_FIPS_CODE,
    "primary_place_of_performance_state_name" as PRIMARY_PLACE_OF_PERFORMANCE_STATE_NAME,
    "primary_place_of_performance_zip_4" as PRIMARY_PLACE_OF_PERFORMANCE_ZIP_4,
    "prime_award_transaction_place_of_performance_cd_original" as PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_CD_ORIGINAL,
    "prime_award_transaction_place_of_performance_cd_current" as PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_CD_CURRENT,
    "primary_place_of_performance_foreign_location" as PRIMARY_PLACE_OF_PERFORMANCE_FOREIGN_LOCATION,
    "cfda_number" as CFDA_NUMBER,
    "cfda_title" as CFDA_TITLE,
    "funding_opportunity_number" as FUNDING_OPPORTUNITY_NUMBER,
    "funding_opportunity_goals_text" as FUNDING_OPPORTUNITY_GOALS_TEXT,
    "assistance_type_code" as ASSISTANCE_TYPE_CODE,
    "assistance_type_description" as ASSISTANCE_TYPE_DESCRIPTION,
    "transaction_description" as TRANSACTION_DESCRIPTION,
    "prime_award_base_transaction_description" as PRIME_AWARD_BASE_TRANSACTION_DESCRIPTION,
    "business_funds_indicator_code" as BUSINESS_FUNDS_INDICATOR_CODE,
    "business_funds_indicator_description" as BUSINESS_FUNDS_INDICATOR_DESCRIPTION,
    "business_types_code" as BUSINESS_TYPES_CODE,
    "business_types_description" as BUSINESS_TYPES_DESCRIPTION,
    "correction_delete_indicator_code" as CORRECTION_DELETE_INDICATOR_CODE,
    "correction_delete_indicator_description" as CORRECTION_DELETE_INDICATOR_DESCRIPTION,
    "action_type_code" as ACTION_TYPE_CODE,
    "action_type_description" as ACTION_TYPE_DESCRIPTION,
    "record_type_code" as RECORD_TYPE_CODE,
    "record_type_description" as RECORD_TYPE_DESCRIPTION,
    "highly_compensated_officer_1_name" as HIGHLY_COMPENSATED_OFFICER_1_NAME,
    try_to_double("highly_compensated_officer_1_amount") as HIGHLY_COMPENSATED_OFFICER_1_AMOUNT,
    "highly_compensated_officer_2_name" as HIGHLY_COMPENSATED_OFFICER_2_NAME,
    try_to_double("highly_compensated_officer_2_amount") as HIGHLY_COMPENSATED_OFFICER_2_AMOUNT,
    "highly_compensated_officer_3_name" as HIGHLY_COMPENSATED_OFFICER_3_NAME,
    try_to_double("highly_compensated_officer_3_amount") as HIGHLY_COMPENSATED_OFFICER_3_AMOUNT,
    "highly_compensated_officer_4_name" as HIGHLY_COMPENSATED_OFFICER_4_NAME,
    try_to_double("highly_compensated_officer_4_amount") as HIGHLY_COMPENSATED_OFFICER_4_AMOUNT,
    "highly_compensated_officer_5_name" as HIGHLY_COMPENSATED_OFFICER_5_NAME,
    try_to_double("highly_compensated_officer_5_amount") as HIGHLY_COMPENSATED_OFFICER_5_AMOUNT,
    "usaspending_permalink" as USASPENDING_PERMALINK,
    try_to_date("initial_report_date") as INITIAL_REPORT_DATE,
    try_to_date("last_modified_date") as LAST_MODIFIED_DATE
from source
