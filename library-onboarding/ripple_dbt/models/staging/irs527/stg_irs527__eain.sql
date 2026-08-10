{{ config(materialized='view') }}

/*
  Generated 2026-08-09 (73-source backlog, wave 2b) from live-verified specs.
  IRS Form 8871 election authority identification numbers: one row per EAIN per form (form_id + eain_id unique).
  Grain: one row = one EAIN listing.
*/

with source as (
    select * from {{ source('ripple_raw', 'IRS527_EAIN') }}
),

renamed as (
    select
        nullif(trim(FORM_ID_NUMBER), '')                               as form_id_number,
        nullif(trim(EAIN_ID), '')                                      as eain_id,
        nullif(trim(ELECTION_AUTHORITY_ID_NUMBER), '')                 as election_authority_id_number,
        nullif(trim(STATE_ISSUED), '')                                 as state_issued,
        to_timestamp_ntz(INGESTED_AT, 6)                               as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                                as _source_run_id
    from source
)

select * from renamed
