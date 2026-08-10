{{ config(materialized='view') }}

/*
  Hand-built 2026-08-09 (73-source backlog). ICE detainers (requests to local
  jails/prisons to hold a person for ICE), person-level with anonymized hash
  IDs, Oct 2022 - 2026, from the Deportation Data Project's cleaned releases.
  Grain: one row = one detainer record as published. person_hash repeats
  (multiple detainers per person: 609,769 rows / 407,078 people) and even
  (person, prepare date, facility) is not unique — rows are only unique with
  file+row provenance. Kept as landed, no dedup; the publisher's
  duplicate_likely flag is carried through (blank on ~75k rows).
  Some prepare dates run slightly past the publication date as landed.
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_ICE_DETAINERS') }}
),

renamed as (
    select
        nullif(trim(UNIQUE_IDENTIFIER), '')                       as person_hash,
        try_to_date(trim(DETAINER_PREPARE_DATE))                  as detainer_prepare_date,
        nullif(trim(DETAINER_TYPE), '')                           as detainer_type,
        nullif(trim(DETENTION_FACILITY), '')                      as detention_facility,
        nullif(trim(DETENTION_FACILITY_CODE), '')                 as detention_facility_code,
        nullif(trim(FACILITY_CITY), '')                           as facility_city,
        nullif(trim(FACILITY_STATE), '')                          as facility_state,
        nullif(trim(FACILITY_AOR), '')                            as facility_aor,
        nullif(trim(GENDER), '')                                  as gender,
        try_to_number(trim(BIRTH_YEAR))                           as birth_year,
        nullif(trim(BIRTH_COUNTRY), '')                           as birth_country,
        nullif(trim(CITIZENSHIP_COUNTRY), '')                     as citizenship_country,
        nullif(trim(ENTRY_STATUS), '')                            as entry_status,
        try_to_date(trim(ENTRY_DATE))                             as entry_date,
        nullif(trim(DETAINER_PREPARED_CRIMINALITY), '')           as detainer_prepared_criminality,
        nullif(trim(DETAINER_PREP_THREAT_LEVEL), '')              as detainer_prep_threat_level,
        nullif(trim(MOST_SERIOUS_CONVICTION_CHARGE), '')          as most_serious_conviction_charge,
        nullif(trim(MSC_CHARGE_CODE), '')                         as msc_charge_code,
        try_to_date(trim(MSC_CHARGE_DATE))                        as msc_charge_date,
        try_to_date(trim(MSC_CONVICTION_DATE))                    as msc_conviction_date,
        try_to_number(trim(MSC_SENTENCE_DAYS))                    as msc_sentence_days,
        try_to_number(trim(MSC_SENTENCE_MONTHS))                  as msc_sentence_months,
        try_to_number(trim(MSC_SENTENCE_YEARS))                   as msc_sentence_years,
        nullif(trim(FELON), '')                                   as felon,
        nullif(trim(PRIOR_FELONY_YES_NO), '')                     as prior_felony_yes_no,
        nullif(trim(MULTIPLE_PRIOR_MISD_YES_NO), '')              as multiple_prior_misd_yes_no,
        nullif(trim(VIOLENT_MISDEMEANOR_YES_NO), '')              as violent_misdemeanor_yes_no,
        nullif(trim(AGGRAVATED_FELONY_YES_NO), '')                as aggravated_felony_yes_no,
        nullif(trim(CRIMINAL_STREET_GANG_YES_NO), '')             as criminal_street_gang_yes_no,
        nullif(trim(ILLEGAL_ENTRY_YES_NO), '')                    as illegal_entry_yes_no,
        nullif(trim(ILLEGAL_REENTRY_YES_NO), '')                  as illegal_reentry_yes_no,
        nullif(trim(IMMIGRATION_FRAUD_YES_NO), '')                as immigration_fraud_yes_no,
        nullif(trim(SIGNIFICANT_RISK_YES_NO), '')                 as significant_risk_yes_no,
        nullif(trim(OTHER_REMOVAL_REASON_YES_NO), '')             as other_removal_reason_yes_no,
        nullif(trim(DEPORTATION_ORDERED_YES_NO), '')              as deportation_ordered_yes_no,
        nullif(trim(ORDER_SHOW_CAUSE_SERVED_YES_NO), '')          as order_show_cause_served_yes_no,
        nullif(trim(BIOMETRIC_MATCH_YES_NO), '')                  as biometric_match_yes_no,
        nullif(trim(STATEMENTS_MADE_YES_NO), '')                  as statements_made_yes_no,
        nullif(trim(UNLAWFUL_ATTEMPT_YES_NO), '')                 as unlawful_attempt_yes_no,
        nullif(trim(UNLAWFUL_ENTRY_YES_NO), '')                   as unlawful_entry_yes_no,
        nullif(trim(VISA_YES_NO), '')                             as visa_yes_no,
        nullif(trim(FEDERAL_INTEREST_YES_NO), '')                 as federal_interest_yes_no,
        nullif(trim(RESUME_CUSTODY_YES_NO), '')                   as resume_custody_yes_no,
        nullif(trim(ACTIVE_INVESTIGATION_YES_NO), '')             as active_investigation_yes_no,
        nullif(trim(NOTIFY_RELEASE_REQUEST_YES_NO), '')           as notify_release_request_yes_no,
        nullif(trim(PROCESSING_DISPOSITION), '')                  as processing_disposition,
        nullif(trim(CASE_STATUS), '')                             as case_status,
        nullif(trim(CASE_CATEGORY), '')                           as case_category,
        nullif(trim(ARREST_TIME_CASE_CATEGORY), '')               as arrest_time_case_category,
        nullif(trim(ARREST_TIME_CURRENT_PROGRAM), '')             as arrest_time_current_program,
        nullif(trim(APPREHENSION_METHOD), '')                     as apprehension_method,
        try_to_timestamp_tz(trim(APPREHENSION_DATE))::timestamp_ntz as apprehension_at,
        nullif(trim(FINAL_ORDER_YES_NO), '')                      as final_order_yes_no,
        try_to_date(trim(FINAL_ORDER_DATE))                       as final_order_date,
        try_to_date(trim(DEPARTED_DATE))                          as departed_date,
        nullif(trim(DEPARTURE_COUNTRY), '')                       as departure_country,
        nullif(trim(PORT_OF_DEPARTURE), '')                       as port_of_departure,
        nullif(trim(DETAINER_LIFT_REASON), '')                    as detainer_lift_reason,
        nullif(trim(DETAINER_LIFT_REASON_CODE), '')               as detainer_lift_reason_code,
        nullif(trim(TOD_CURRENT_DUTY_SITE), '')                   as tod_current_duty_site,
        nullif(trim(DUPLICATE_LIKELY), '')                        as duplicate_likely,
        nullif(trim(FILE_ORIGINAL), '')                           as file_original,
        nullif(trim(SHEET_ORIGINAL), '')                          as sheet_original,
        nullif(trim(ROW_ORIGINAL), '')                            as row_original,
        to_timestamp_ntz(INGESTED_AT)                             as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                           as _source_run_id
    from source
)

select * from renamed
