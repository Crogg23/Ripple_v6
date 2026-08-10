{{ config(materialized='view') }}

/*
  Generated 2026-08-09 (73-source backlog, wave 2b) from live-verified specs.
  CAL-ACCESS lobbyist campaign contributions: one row per reported contribution. CONTRIBUTION_DT blank on many rows as published.
  Grain: one row = one reported contribution (no unique key).
*/

with source as (
    select * from {{ source('ripple_raw', 'CA_LOBBY_CONTRIBUTIONS') }}
),

renamed as (
    select
        nullif(trim(FILER_ID), '')                                     as filer_id,
        try_to_date(split_part(nullif(trim(FILING_PERIOD_START_DT), ''), ' ', 1), 'MM/DD/YYYY') as filing_period_start_dt,
        try_to_date(split_part(nullif(trim(FILING_PERIOD_END_DT), ''), ' ', 1), 'MM/DD/YYYY') as filing_period_end_dt,
        try_to_date(split_part(nullif(trim(CONTRIBUTION_DT), ''), ' ', 1), 'MM/DD/YYYY') as contribution_dt,
        nullif(trim(RECIPIENT_NAME), '')                               as recipient_name,
        nullif(trim(RECIPIENT_ID), '')                                 as recipient_id,
        try_to_number(nullif(trim(AMOUNT), ''), 18, 2)                 as amount,
        to_timestamp_ntz(INGESTED_AT, 6)                               as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                                as _source_run_id
    from source
)

select * from renamed
