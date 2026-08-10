{{ config(materialized='view') }}

/*
  Generated 2026-08-10 (backlog wave 4) from live-verified specs.
  NLM DailyMed Structured Product Labeling (SPL) set-id to label file map:
  which SPL zip file and version carries each drug label set id.
  Grain: one row = one SPL set id (SETID verified exactly unique).
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_NLM_DAILYMED_SPL_SETID_MAP') }}
),

renamed as (
    select
        -- identifiers
        nullif(trim(SETID), '')                                    as setid,

        -- label file map
        nullif(trim(ZIP_FILE_NAME), '')                            as zip_file_name,
        try_to_date(nullif(trim(UPLOAD_DATE), ''))                 as upload_date,
        try_to_number(trim(SPL_VERSION))                           as spl_version,
        nullif(trim(TITLE), '')                                    as title,

        -- metadata
        to_timestamp_ntz(INGESTED_AT, 6)                           as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                            as _source_run_id
    from source
)

select * from renamed
