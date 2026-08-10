{{ config(materialized='view') }}

/*
  Generated 2026-08-09 (73-source backlog, wave 2b) from live-verified specs.
  CAL-ACCESS lobbying registration change log: one row per logged attribute change. filer_id+change_no has 11 published near-duplicates -- no unique test.
  Grain: one row = one logged change (no unique key as published).
*/

with source as (
    select * from {{ source('ripple_raw', 'CA_LOBBY_CHG_LOG') }}
),

renamed as (
    select
        nullif(trim(FILER_ID), '')                                     as filer_id,
        nullif(trim(CHANGE_NO), '')                                    as change_no,
        nullif(trim(SESSION_ID), '')                                   as session_id,
        try_to_date(split_part(nullif(trim(LOG_DT), ''), ' ', 1), 'MM/DD/YYYY') as log_dt,
        nullif(trim(FILER_TYPE), '')                                   as filer_type,
        nullif(trim(CORRECTION_FLG), '')                               as correction_flg,
        nullif(trim(ACTION), '')                                       as action,
        nullif(trim(ATTRIBUTE_CHANGED), '')                            as attribute_changed,
        try_to_date(split_part(nullif(trim(ETHICS_DT), ''), ' ', 1), 'MM/DD/YYYY') as ethics_dt,
        nullif(trim(INTERESTS), '')                                    as interests,
        nullif(trim(FILER_FULL_NAME), '')                              as filer_full_name,
        nullif(trim(FILER_CITY), '')                                   as filer_city,
        nullif(trim(FILER_ST), '')                                     as filer_st,
        nullif(trim(FILER_ZIP), '')                                    as filer_zip,
        nullif(trim(FILER_PHONE), '')                                  as filer_phone,
        nullif(trim(ENTITY_TYPE), '')                                  as entity_type,
        nullif(trim(ENTITY_NAME), '')                                  as entity_name,
        nullif(trim(ENTITY_CITY), '')                                  as entity_city,
        nullif(trim(ENTITY_ST), '')                                    as entity_st,
        nullif(trim(ENTITY_ZIP), '')                                   as entity_zip,
        nullif(trim(ENTITY_PHONE), '')                                 as entity_phone,
        nullif(trim(ENTITY_ID), '')                                    as entity_id,
        nullif(trim(RESPONSIBLE_OFFICER), '')                          as responsible_officer,
        try_to_date(split_part(nullif(trim(EFFECT_DT), ''), ' ', 1), 'MM/DD/YYYY') as effect_dt,
        to_timestamp_ntz(INGESTED_AT, 6)                               as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                                as _source_run_id
    from source
)

select * from renamed
