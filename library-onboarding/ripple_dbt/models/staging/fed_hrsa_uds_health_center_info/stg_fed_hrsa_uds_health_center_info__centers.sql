{{ config(materialized='view') }}

/*
  Generated 2026-08-09 (73-source backlog, wave 2c) from live-verified specs.
  HRSA UDS health center directory: one row per federally-funded health center (bhcmisid unique) with address, director, funding streams, urban/rural flag.
  Grain: one row = one health center.
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_HRSA_UDS_HEALTH_CENTER_INFO') }}
),

renamed as (
    select
        nullif(trim(BHCMISID), '')                                 as bhcmisid,
        nullif(trim(GRANTNUMBER), '')                              as grantnumber,
        nullif(trim(REPORTINGYEAR), '')                            as reportingyear,
        nullif(trim(HEALTHCENTERNAME), '')                         as healthcentername,
        nullif(trim(HEALTHCENTERSTREETADDRESS), '')                as healthcenterstreetaddress,
        nullif(trim(HEALTHCENTEROTHERADDRESS), '')                 as healthcenterotheraddress,
        nullif(trim(HEALTHCENTERCITY), '')                         as healthcentercity,
        nullif(trim(HEALTHCENTERSTATE), '')                        as healthcenterstate,
        nullif(trim(HEALTHCENTERZIPCODE), '')                      as healthcenterzipcode,
        nullif(trim(PROJECTDIRECTOR), '')                          as projectdirector,
        nullif(trim(PROJECTDIRECTORPHONE), '')                     as projectdirectorphone,
        nullif(trim(PROJECTDIRECTORPHONEEXT), '')                  as projectdirectorphoneext,
        nullif(trim(PROJECTDIRECTORFAX), '')                       as projectdirectorfax,
        nullif(trim(PROJECTDIRECTOREMAIL), '')                     as projectdirectoremail,
        nullif(trim(FUNDINGCHC), '')                               as fundingchc,
        nullif(trim(FUNDINGMSAW), '')                              as fundingmsaw,
        nullif(trim(FUNDINGHP), '')                                as fundinghp,
        nullif(trim(FUNDINGRPH), '')                               as fundingrph,
        nullif(trim(URBANRURALFLAG), '')                           as urbanruralflag,
        to_timestamp_ntz(_INGESTED_AT, 6)                          as _ingested_at,
        nullif(trim(_SOURCE_RUN_ID), '')                           as _source_run_id
    from source
)

select * from renamed
