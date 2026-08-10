{{ config(materialized='view') }}

/*
  Generated 2026-08-09 (73-source backlog, wave 2d).
  SAMPLE ONLY -- NOT the full dataset. USAspending subawards: a 5,000-row API slice of the multi-million-row subaward corpus, landed as flat JSON records. Use for shape/testing only.
  Grain: one row = one subaward record (id unique in the slice).
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_USASPENDING_SUBAWARDS') }}
),

parsed as (
    select
        parse_json(RECORD):id::string                    as subaward_id,
        parse_json(RECORD):subaward_number::string       as subaward_number,
        parse_json(RECORD):recipient_name::string        as recipient_name,
        try_to_number(parse_json(RECORD):amount::string, 18, 2) as amount,
        try_to_date(parse_json(RECORD):action_date::string)     as action_date,
        parse_json(RECORD):description::string           as description,
        parse_json(RECORD)                               as record_json,
        to_timestamp_ntz(_INGESTED_AT)                   as _ingested_at,
        nullif(trim(_SOURCE_RUN_ID), '')                 as _source_run_id
    from source
)

select * from parsed
