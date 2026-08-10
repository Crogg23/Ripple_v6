{{ config(materialized='view') }}

/*
  Hand-built 2026-08-09 for the dead-source rebuild sprint (fed_fra_casualties).
  Grain: one row = one reported rail-related casualty (Form 55a); REPORT_KEY verified unique (1,150,788 = 1,150,788)
  No dedup: landing is a full-replace Socrata export.
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_FRA_CASUALTIES') }}
),

renamed as (
    select
        nullif(trim("RAILROAD_CODE"), '') as railroad_code,
        nullif(trim("RAILROAD_NAME"), '') as railroad_name,
        nullif(trim("PDF_REPORT"), '') as pdf_report,
        nullif(trim("INCIDENT_NUMBER"), '') as incident_number,
        try_to_number(replace(trim("INCIDENT_YEAR"), ',', '')) as incident_year,
        nullif(trim("INCIDENT_MONTH"), '') as incident_month,
        nullif(trim("INCIDENT_DAY"), '') as incident_day,
        try_to_date(trim("DATE"), 'MM/DD/YYYY') as date,
        nullif(trim("TIME"), '') as time,
        nullif(trim("COUNTY_CODE"), '') as county_code,
        nullif(trim("COUNTY_NAME"), '') as county_name,
        nullif(trim("STATE_CODE"), '') as state_code,
        nullif(trim("STATE_NAME"), '') as state_name,
        nullif(trim("TYPE_OF_PERSON_CODE"), '') as type_of_person_code,
        nullif(trim("TYPE_OF_PERSON"), '') as type_of_person,
        nullif(trim("EMPLOYEE_JOB_CODE"), '') as employee_job_code,
        nullif(trim("EMPLOYEE_JOB_DESCRIPTION"), '') as employee_job_description,
        try_to_number(replace(trim("AGE_OF_PERSON"), ',', '')) as age_of_person,
        try_to_number(replace(trim("POSITIVE_ALCOHOL_TESTS"), ',', '')) as positive_alcohol_tests,
        try_to_number(replace(trim("POSITIVE_DRUG_TESTS"), ',', '')) as positive_drug_tests,
        nullif(trim("INJURY_ILLNESS_CODE"), '') as injury_illness_code,
        nullif(trim("NATURE_OF_INJURY"), '') as nature_of_injury,
        nullif(trim("LOCATION_OF_INJURY_ON_BODY"), '') as location_of_injury_on_body,
        nullif(trim("SPECIFIC_LOCATION"), '') as specific_location,
        nullif(trim("INJURY_ILLNESS"), '') as injury_illness,
        nullif(trim("PHYSICAL_ACT_CIRCUMSTANCES_CODE"), '') as physical_act_circumstances_code,
        nullif(trim("PHYSICAL_ACT_CIRCUMSTANCES"), '') as physical_act_circumstances,
        nullif(trim("GENERAL_LOCATION_OF_PERSON_CODE"), '') as general_location_of_person_code,
        nullif(trim("GENERAL_LOCATION_OF_PERSON"), '') as general_location_of_person,
        nullif(trim("ON_TRACK_EQUIPMENT_CODE"), '') as on_track_equipment_code,
        nullif(trim("ON_TRACK_EQUIPMENT"), '') as on_track_equipment,
        nullif(trim("SPECIFIC_LOCATION_OF_PERSON_CODE"), '') as specific_location_of_person_code,
        nullif(trim("SPECIFIC_LOCATION_OF_PERSON"), '') as specific_location_of_person,
        nullif(trim("EVENT_CODE"), '') as event_code,
        nullif(trim("EVENT"), '') as event,
        nullif(trim("TOOLS_CODE"), '') as tools_code,
        nullif(trim("TOOLS"), '') as tools,
        nullif(trim("INJURY_CAUSE_CODE"), '') as injury_cause_code,
        nullif(trim("INJURY_CAUSE"), '') as injury_cause,
        try_to_number(replace(trim("DAYS_AWAY_FROM_WORK"), ',', '')) as days_away_from_work,
        try_to_number(replace(trim("DAYS_RESTRICTED_ACTIVITY"), ',', '')) as days_restricted_activity,
        nullif(trim("HAZMAT_EXPOSURE"), '') as hazmat_exposure,
        nullif(trim("COVERED_DATA_CODE"), '') as covered_data_code,
        nullif(trim("COVERED_DATA_REASON"), '') as covered_data_reason,
        try_to_double(replace(trim("LATITUDE"), ',', '')) as latitude,
        try_to_double(replace(trim("LONGITUDE"), ',', '')) as longitude,
        nullif(trim("NARRATIVE"), '') as narrative,
        nullif(trim("EMPLOYEE_SUSPENSION"), '') as employee_suspension,
        nullif(trim("DISTRICT"), '') as district,
        nullif(trim("FATALITY"), '') as fatality,
        nullif(trim("FORM_57_FILED"), '') as form_57_filed,
        nullif(trim("FORM_54_FILED"), '') as form_54_filed,
        nullif(trim("CLASS_CODE"), '') as class_code,
        nullif(trim("CLASS"), '') as class,
        nullif(trim("CASUALTY_OCCURRENCE_CODE"), '') as casualty_occurrence_code,
        nullif(trim("EQUIPMENT_MOVEMENT_CODE"), '') as equipment_movement_code,
        nullif(trim("REPORT_KEY"), '') as report_key,
        nullif(trim("REPORTING_RAILROAD_SMT_GROUPING"), '') as reporting_railroad_smt_grouping,
        nullif(trim("REPORTING_PARENT_RAILROAD_CODE"), '') as reporting_parent_railroad_code,
        nullif(trim("REPORTING_PARENT_RAILROAD_NAME"), '') as reporting_parent_railroad_name,
        nullif(trim("REPORTING_RAILROAD_HOLDING_COMPANY"), '') as reporting_railroad_holding_company,
        nullif(trim("GEOCODE"), '') as geocode,
        nullif(trim("INCIDENT_KEY"), '') as incident_key,
        nullif(trim("REPORTING_RAILROAD_INDIVIDUAL_CLASS"), '') as reporting_railroad_individual_class,
        nullif(trim("REPORTING_RAILROAD_PASSENGER"), '') as reporting_railroad_passenger,
        nullif(trim("REPORTING_RAILROAD_COMMUTER"), '') as reporting_railroad_commuter,
        nullif(trim("REPORTING_RAILROAD_SWITCHING_TERMINAL"), '') as reporting_railroad_switching_terminal,
        nullif(trim("REPORTING_RAILROAD_TOURIST"), '') as reporting_railroad_tourist,
        nullif(trim("REPORTING_RAILROAD_FREIGHT"), '') as reporting_railroad_freight,
        nullif(trim("REPORTING_RAILROAD_SHORT_LINE"), '') as reporting_railroad_short_line,
        to_timestamp_ntz(_INGESTED_AT, 6) as _ingested_at,
        nullif(trim(_SOURCE_RUN_ID), '') as _source_run_id
    from source
)

select * from renamed
