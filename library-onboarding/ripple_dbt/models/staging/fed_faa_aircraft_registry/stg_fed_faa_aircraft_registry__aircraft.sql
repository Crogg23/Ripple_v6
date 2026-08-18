{{ config(materialized='view') }}

/*
  Hand-built 2026-08-09 (73-source backlog, wave 2). FAA Civil Aircraft
  Registry master file (2026-08 vintage; supersedes the July FED_FAA_REGISTRY
  twin, which is queued for the orphan drop list with its old mart).
  Grain: one row = one registered aircraft; N_NUMBER and UNIQUE_ID both
  verified unique (315,447 = 315,447).
  Source is a fixed-width-style CSV: every field space-padded (trim all);
  dates are YYYYMMDD strings with blanks (YEAR_MFR blank on ~22%,
  AIR_WORTH_DATE blank on ~14%).
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_FAA_AIRCRAFT_REGISTRY') }}
),

renamed as (
    select
        nullif(trim(N_NUMBER), '')                             as n_number,
        nullif(trim(SERIAL_NUMBER), '')                        as serial_number,
        nullif(trim(MFR_MDL_CODE), '')                         as mfr_mdl_code,
        nullif(trim(ENG_MFR_MDL), '')                          as eng_mfr_mdl,
        try_to_number(nullif(trim(YEAR_MFR), ''))              as year_mfr,
        nullif(trim(TYPE_REGISTRANT), '')                      as type_registrant,
        nullif(trim(NAME), '')                                 as registrant_name,
        nullif(trim(STREET), '')                               as street,
        nullif(trim(STREET2), '')                              as street2,
        nullif(trim(CITY), '')                                 as city,
        nullif(trim(STATE), '')                                as state,
        nullif(trim(ZIP_CODE), '')                             as zip_code,
        nullif(trim(REGION), '')                               as region,
        nullif(trim(COUNTY), '')                               as county_code,
        nullif(trim(COUNTRY), '')                              as country_code,
        try_to_date(nullif(trim(LAST_ACTION_DATE), ''), 'YYYYMMDD') as last_action_date,
        try_to_date(nullif(trim(CERT_ISSUE_DATE), ''), 'YYYYMMDD')  as cert_issue_date,
        nullif(trim(CERTIFICATION), '')                        as certification_codes,
        nullif(trim(TYPE_AIRCRAFT), '')                        as type_aircraft,
        nullif(trim(TYPE_ENGINE), '')                          as type_engine,
        nullif(trim(STATUS_CODE), '')                          as status_code,
        nullif(trim(MODE_S_CODE), '')                          as mode_s_code,
        nullif(trim(FRACT_OWNER), '')                          as fractional_owner,
        -- NOT A BUG, NOT A REGRESSION (epoch-1970 investigation, 2026-08-18):
        -- already uses the explicit 'YYYYMMDD' format fixed 2026-08-09 (see the
        -- mart header). Re-checked live this session: 2,325-of-315,447 (0.7%)
        -- rows in 1970 spread across ~230 distinct days that whole year -- real
        -- 50+ year old aircraft still on the registry, not sentinel garbage.
        try_to_date(nullif(trim(AIR_WORTH_DATE), ''), 'YYYYMMDD')   as airworthiness_date,
        nullif(trim(OTHER_NAMES_1), '')                        as other_name_1,
        nullif(trim(OTHER_NAMES_2), '')                        as other_name_2,
        nullif(trim(OTHER_NAMES_3), '')                        as other_name_3,
        nullif(trim(OTHER_NAMES_4), '')                        as other_name_4,
        nullif(trim(OTHER_NAMES_5), '')                        as other_name_5,
        try_to_date(nullif(trim(EXPIRATION_DATE), ''), 'YYYYMMDD')  as expiration_date,
        nullif(trim(UNIQUE_ID), '')                            as unique_id,
        nullif(trim(KIT_MFR), '')                              as kit_mfr,
        nullif(trim(KIT_MODEL), '')                            as kit_model,
        nullif(trim(MODE_S_CODE_HEX), '')                      as mode_s_code_hex,
        to_timestamp_ntz(_INGESTED_AT, 6)                      as _ingested_at,
        nullif(trim(_SOURCE_RUN_ID), '')                       as _source_run_id
    from source
)

select * from renamed
