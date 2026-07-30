{{ config(materialized='table', schema='INVESTIGATIONS') }}

-- GRAIN: one row per link scraped from an archived DOJ listing page capture
-- Answers: which files each archived DOJ listing page pointed at, and at what capture
--          -- i.e. what was on the page before it changed
-- Source: Wayback replay of DOJ Epstein listing pages (24,897 links)
--
-- FIXED 2026-07-29: was `select RECORD as record`, a single untyped VARIANT column.

with source as (

    select * from {{ source('ripple_raw', 'XC_WAYBACK_REPLAY_DOJ_LISTING') }}

)

select
    RECORD:page_url::string      as page_url,
    RECORD:page_digest::string   as page_digest,
    RECORD:capture_timestamp::string as capture_timestamp_raw,
    try_to_timestamp_ntz(RECORD:capture_timestamp::string, 'YYYYMMDDHH24MISS') as captured_at,
    RECORD:href::string          as href,
    RECORD:url::string           as resolved_url,
    RECORD:link_text::string     as link_text,
    try_to_timestamp_ntz(RECORD:fetched_at_utc::string) as fetched_at_utc,
    _INGESTED_AT                 as _loaded_at

from source
where RECORD:url is not null
