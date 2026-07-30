{{ config(materialized='table', schema='OPEN_DATA') }}

-- GRAIN: one row per Wayback Machine capture (URLKEY + CAPTURE_TIMESTAMP)
-- Answers: which DOJ Epstein-library URLs existed, when they were captured, and
--          whether a given capture returned content or an error
-- Source: Wayback CDX census of DOJ Epstein library listing pages (1.54M captures)
--
-- FIXED 2026-07-29: this mart used to be `select RECORD as record` -- a single
-- untyped VARIANT column. Nothing could filter or join it, so 1.54M captures were
-- effectively unreadable while the source still counted as a modelled mart. The CDX
-- fields are flat, so they are now typed out properly.

with source as (

    select * from {{ source('ripple_raw', 'XC_WAYBACK_DOJ_EPSTEIN') }}

)

select
    RECORD:urlkey::string      as urlkey,
    RECORD:original::string    as original_url,
    RECORD:timestamp::string   as capture_timestamp_raw,
    -- CDX timestamps are YYYYMMDDHHMISS in UTC
    try_to_timestamp_ntz(RECORD:timestamp::string, 'YYYYMMDDHH24MISS') as captured_at,
    RECORD:mimetype::string    as mimetype,
    RECORD:statuscode::string  as status_code,
    RECORD:digest::string      as content_digest,
    try_to_number(RECORD:length::string) as content_length_bytes,
    _INGESTED_AT               as _loaded_at

from source
where RECORD:urlkey is not null
