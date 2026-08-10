{{ config(materialized='view') }}

/*
  Generated 2026-08-09 (73-source backlog, wave 2d).
  SAMPLE ONLY -- NOT the full dataset. EPA Envirofacts API: a 5,000-row slice of ONE program table (TRI facility names); FRS/site/handler id columns are blank in this slice. Use for shape/testing only.
  Grain: one row = one facility-name row from the TRI slice (no key).
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_EPA_ENVIROFACTS') }}
),

renamed as (
    select
        nullif(trim(TABLE_NAME), '')                               as table_name,
        nullif(trim(PROGRAM_SCHEMA), '')                           as program_schema,
        nullif(trim(STATE_CODE), '')                               as state_code,
        nullif(trim(CITY_NAME), '')                                as city_name,
        nullif(trim(POSTAL_CODE), '')                              as postal_code,
        nullif(trim(COUNTY_NAME), '')                              as county_name,
        nullif(trim(FRS_ID), '')                                   as frs_id,
        nullif(trim(HANDLER_ID), '')                               as handler_id,
        nullif(trim(SITE_ID), '')                                  as site_id,
        nullif(trim(FACILITY_NAME), '')                            as facility_name,
        nullif(trim(LATITUDE), '')                                 as latitude,
        nullif(trim(LONGITUDE), '')                                as longitude,
        nullif(trim(CREATED_DATE), '')                             as created_date,
        nullif(trim(MEDIA_NAME), '')                               as media_name,
        to_timestamp_ntz(_INGESTED_AT, 6)                          as _ingested_at,
        nullif(trim(_SOURCE_RUN_ID), '')                           as _source_run_id
    from source
)

select * from renamed
