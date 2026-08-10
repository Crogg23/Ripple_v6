{{ config(materialized='view') }}

/*
  Generated 2026-08-09 (73-source backlog, wave 2b) from live-verified specs.
  Texas lobby on-behalf-of lines: one row per client an expenditure was made on behalf of (lobbyexpendonbehalfid unique).
  Grain: one row = one on-behalf-of line.
*/

with source as (
    select * from {{ source('ripple_raw', 'TX_LOBBY_INDIVIDUAL_REPORTING') }}
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
        nullif(trim(LOBBYEXPENDONBEHALFID), '')                        as on_behalf_id,
        nullif(trim(ONBEHALFNAME), '')                                 as onbehalfname,
        nullif(trim(ONBEHALFMAILINGADDR1), '')                         as onbehalfmailingaddr1,
        nullif(trim(ONBEHALFMAILINGADDR2), '')                         as onbehalfmailingaddr2,
        nullif(trim(ONBEHALFMAILINGCITY), '')                          as onbehalfmailingcity,
        nullif(trim(ONBEHALFMAILINGSTATECD), '')                       as onbehalfmailingstatecd,
        nullif(trim(ONBEHALFMAILINGCOUNTYCD), '')                      as onbehalfmailingcountycd,
        nullif(trim(ONBEHALFMAILINGCOUNTRYCD), '')                     as onbehalfmailingcountrycd,
        nullif(trim(ONBEHALFMAILINGPOSTALCODE), '')                    as onbehalfmailingpostalcode,
        nullif(trim(ONBEHALFMAILINGREGION), '')                        as onbehalfmailingregion,
        nullif(trim(ONBEHALFPRIMARYUSAPHONEFLAG), '')                  as onbehalfprimaryusaphoneflag,
        nullif(trim(ONBEHALFPRIMARYPHONENUMBER), '')                   as onbehalfprimaryphonenumber,
        nullif(trim(ONBEHALFPRIMARYPHONEEXT), '')                      as onbehalfprimaryphoneext,
        to_timestamp_ntz(INGESTED_AT, 6)                               as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                                as _source_run_id
    from source
)

select * from renamed
