{{ config(materialized='view') }}

/*
  Generated 2026-08-09 (73-source backlog, wave 2b) from live-verified specs.
  CAL-ACCESS in-house lobbyist roster: one row per lobbyist-employer-session (unique).
  Grain: one row = one lobbyist-employer-session.
*/

with source as (
    select * from {{ source('ripple_raw', 'CA_LOBBY_EMP_LOBBYIST') }}
),

renamed as (
    select
        nullif(trim(LOBBYIST_ID), '')                                  as lobbyist_id,
        nullif(trim(EMPLOYER_ID), '')                                  as employer_id,
        nullif(trim(LOBBYIST_LAST_NAME), '')                           as lobbyist_last_name,
        nullif(trim(LOBBYIST_FIRST_NAME), '')                          as lobbyist_first_name,
        nullif(trim(EMPLOYER_NAME), '')                                as employer_name,
        nullif(trim(SESSION_ID), '')                                   as session_id,
        to_timestamp_ntz(INGESTED_AT, 6)                               as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                                as _source_run_id
    from source
)

select * from renamed
