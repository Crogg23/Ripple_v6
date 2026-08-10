{{ config(materialized='view') }}

/*
  Generated 2026-08-09 (73-source backlog, wave 2b) from live-verified specs.
  CAL-ACCESS employer-to-firm engagements: one row per employer-firm-session (unique).
  Grain: one row = one employer-firm-session.
*/

with source as (
    select * from {{ source('ripple_raw', 'CA_LOBBY_EMPLOYER_FIRMS') }}
),

renamed as (
    select
        nullif(trim(EMPLOYER_ID), '')                                  as employer_id,
        nullif(trim(FIRM_ID), '')                                      as firm_id,
        nullif(trim(FIRM_NAME), '')                                    as firm_name,
        nullif(trim(SESSION_ID), '')                                   as session_id,
        try_to_date(split_part(nullif(trim(TERMINATION_DT), ''), ' ', 1), 'MM/DD/YYYY') as termination_dt,
        to_timestamp_ntz(INGESTED_AT, 6)                               as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                                as _source_run_id
    from source
)

select * from renamed
