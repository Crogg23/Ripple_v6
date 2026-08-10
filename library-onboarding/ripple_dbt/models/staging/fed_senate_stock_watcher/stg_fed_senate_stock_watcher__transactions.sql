{{ config(materialized='view') }}

/*
  Generated 2026-08-09 (73-source backlog, wave 2c) from live-verified specs.
  Senate Stock Watcher scrape of senator financial-disclosure trades (name-only source, coverage ends Dec 2020; STOCK Act disclosure-use limits apply -- journalism use only). 546 published exact-duplicate rows kept as landed.
  Grain: one row = one reported trade line (no unique key).
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_SENATE_STOCK_WATCHER') }}
),

renamed as (
    select
        try_to_date(nullif(trim(TRANSACTION_DATE), ''), 'MM/DD/YYYY') as transaction_date,
        nullif(trim(OWNER), '')                                    as owner,
        nullif(trim(TICKER), '')                                   as ticker,
        nullif(trim(ASSET_DESCRIPTION), '')                        as asset_description,
        nullif(trim(ASSET_TYPE), '')                               as asset_type,
        nullif(trim(TYPE), '')                                     as type,
        nullif(trim(AMOUNT), '')                                   as amount,
        nullif(trim(COMMENT), '')                                  as comment,
        nullif(trim(SENATOR), '')                                  as senator,
        nullif(trim(PTR_LINK), '')                                 as ptr_link,
        to_timestamp_ntz(_INGESTED_AT, 6)                          as _ingested_at,
        nullif(trim(_SOURCE_RUN_ID), '')                           as _source_run_id
    from source
)

select * from renamed
