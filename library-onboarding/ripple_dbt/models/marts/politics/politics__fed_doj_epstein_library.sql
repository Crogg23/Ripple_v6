{{ config(materialized='table', schema='POLITICS') }}

-- GRAIN: one row per link found on the live DOJ Epstein library pages
-- Answers: what files DOJ published, under what link text, on which page
-- Source: DOJ Epstein Library file manifest (777 links)
--
-- FIXED 2026-07-29: was `select RECORD as record`, a single untyped VARIANT column.

with source as (

    select * from {{ source('ripple_raw', 'FED_DOJ_EPSTEIN_LIBRARY') }}

)

select
    RECORD:page_url::string   as page_url,
    RECORD:href::string       as href,
    RECORD:url::string        as resolved_url,
    RECORD:link_text::string  as link_text,
    try_to_timestamp_ntz(RECORD:fetched_at_utc::string) as fetched_at_utc,
    _INGESTED_AT              as _loaded_at

from source
where RECORD:url is not null
