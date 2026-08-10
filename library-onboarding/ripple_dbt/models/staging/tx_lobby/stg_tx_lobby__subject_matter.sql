{{ config(materialized='view') }}

/*
  Generated 2026-08-09 (73-source backlog, wave 2b) from live-verified specs.
  Texas lobby subject-matter lines: one row per reported subject matter (lobbysubjectmatterid unique).
  Grain: one row = one subject-matter line.
*/

with source as (
    select * from {{ source('ripple_raw', 'TX_LOBBY_SUBJECT_MATTER') }}
),

renamed as (
    select
        nullif(trim(RECORDTYPE), '')                                   as recordtype,
        nullif(trim(FORMTYPECD), '')                                   as formtypecd,
        nullif(trim(REPORTTYPECD), '')                                 as reporttypecd,
        nullif(trim(REPORTINFOIDENT), '')                              as report_id,
        nullif(trim(APPLICABLEYEAR), '')                               as applicableyear,
        nullif(trim(FILERIDENT), '')                                   as filer_id,
        nullif(trim(FILERTYPECD), '')                                  as filertypecd,
        nullif(trim(FILERNAME), '')                                    as filername,
        nullif(trim(FILERSORT), '')                                    as filersort,
        try_to_date(nullif(trim(DUEDT), ''), 'YYYYMMDD')               as duedt,
        try_to_date(nullif(trim(RECEIVEDDT), ''), 'YYYYMMDD')          as receiveddt,
        try_to_date(nullif(trim(PERIODSTARTDT), ''), 'YYYYMMDD')       as periodstartdt,
        try_to_date(nullif(trim(PERIODENDDT), ''), 'YYYYMMDD')         as periodenddt,
        nullif(trim(LOBBYFORMTYPE), '')                                as lobbyformtype,
        nullif(trim(LOBBYSUBJECTMATTERID), '')                         as subject_matter_id,
        nullif(trim(SUBJECTMATTERCD), '')                              as subjectmattercd,
        nullif(trim(SUBJECTMATTERCODEVALUE), '')                       as subjectmattercodevalue,
        nullif(trim(SUBJECTMATTERDESCR), '')                           as subjectmatterdescr,
        to_timestamp_ntz(INGESTED_AT, 6)                               as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                                as _source_run_id
    from source
)

select * from renamed
