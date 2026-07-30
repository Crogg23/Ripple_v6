{{ config(materialized='table', schema='INVESTIGATIONS') }}

-- GRAIN: one row per link scraped from an archived DOJ deep (non-listing) page capture
-- Answers: what the deeper DOJ pages linked to at each capture
-- Source: Wayback replay of DOJ Epstein deep pages (2,542 links)
--
-- FIXED 2026-07-29: was `select RECORD as record`, a single untyped VARIANT column.

with source as (

    select * from {{ source('ripple_raw', 'XC_WAYBACK_REPLAY_DOJ_DEEP_PAGES') }}

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
