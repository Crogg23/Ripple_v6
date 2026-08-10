{{ config(materialized='view') }}

/*
  Hand-built 2026-08-09 for the dead-source rebuild sprint (fed_faa_aircraft_registry).
  Grain: one row = one registered US civil aircraft; trimmed N_NUMBER verified unique (315,447 = 315,447)
  Fixed-width export: every field is space-padded, hence trim() on all columns.
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_FAA_AIRCRAFT_REGISTRY') }}
),

renamed as (
    select
        nullif(trim("N_NUMBER"), '') as n_number,
        nullif(trim("SERIAL_NUMBER"), '') as serial_number,
        nullif(trim("MFR_MDL_CODE"), '') as mfr_mdl_code,
        nullif(trim("ENG_MFR_MDL"), '') as eng_mfr_mdl,
        try_to_number(replace(trim("YEAR_MFR"), ',', '')) as year_mfr,
        nullif(trim("TYPE_REGISTRANT"), '') as type_registrant,
        nullif(trim("NAME"), '') as name,
        nullif(trim("STREET"), '') as street,
        nullif(trim("STREET2"), '') as street2,
        nullif(trim("CITY"), '') as city,
        nullif(trim("STATE"), '') as state,
        nullif(trim("ZIP_CODE"), '') as zip_code,
        nullif(trim("REGION"), '') as region,
        nullif(trim("COUNTY"), '') as county,
        nullif(trim("COUNTRY"), '') as country,
        try_to_date(trim("LAST_ACTION_DATE"), 'YYYYMMDD') as last_action_date,
        try_to_date(trim("CERT_ISSUE_DATE"), 'YYYYMMDD') as cert_issue_date,
        nullif(trim("CERTIFICATION"), '') as certification,
        nullif(trim("TYPE_AIRCRAFT"), '') as type_aircraft,
        nullif(trim("TYPE_ENGINE"), '') as type_engine,
        nullif(trim("STATUS_CODE"), '') as status_code,
        nullif(trim("MODE_S_CODE"), '') as mode_s_code,
        nullif(trim("FRACT_OWNER"), '') as fract_owner,
        try_to_date(trim("AIR_WORTH_DATE"), 'YYYYMMDD') as air_worth_date,
        nullif(trim("OTHER_NAMES_1"), '') as other_names_1,
        nullif(trim("OTHER_NAMES_2"), '') as other_names_2,
        nullif(trim("OTHER_NAMES_3"), '') as other_names_3,
        nullif(trim("OTHER_NAMES_4"), '') as other_names_4,
        nullif(trim("OTHER_NAMES_5"), '') as other_names_5,
        try_to_date(trim("EXPIRATION_DATE"), 'YYYYMMDD') as expiration_date,
        nullif(trim("UNIQUE_ID"), '') as unique_id,
        nullif(trim("KIT_MFR"), '') as kit_mfr,
        nullif(trim("KIT_MODEL"), '') as kit_model,
        nullif(trim("MODE_S_CODE_HEX"), '') as mode_s_code_hex,
        nullif(trim("UNNAMED_34"), '') as unnamed_34,
        to_timestamp_ntz(_INGESTED_AT, 6) as _ingested_at,
        nullif(trim(_SOURCE_RUN_ID), '') as _source_run_id
    from source
)

select * from renamed
