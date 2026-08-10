{{ config(materialized='view') }}

/*
  Generated 2026-08-09 (73-source backlog, wave 2b) from live-verified specs.
  Texas lobby event expenditures (ceremonies/receptions for officials): one row per activity (lobbyactivityid unique).
  Grain: one row = one event activity.
*/

with source as (
    select * from {{ source('ripple_raw', 'TX_LOBBY_EVENTS') }}
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
        nullif(trim(LOBBYACTIVITYID), '')                              as activity_id,
        nullif(trim(CREDITCARDFLAG), '')                               as creditcardflag,
        try_to_date(nullif(trim(ACTIVITYDATE), ''), 'YYYYMMDD')        as activitydate,
        nullif(trim(ACTIVITYDESCRIPTION), '')                          as activitydescription,
        nullif(trim(LOBBYEVENTKINDCD), '')                             as lobbyeventkindcd,
        nullif(trim(RECIPIENTPERSENTTYPECD), '')                       as recipientpersenttypecd,
        nullif(trim(RECIPIENTNAMEORGANIZATION), '')                    as recipientnameorganization,
        nullif(trim(RECIPIENTNAMELAST), '')                            as recipientnamelast,
        nullif(trim(RECIPIENTNAMESUFFIXCD), '')                        as recipientnamesuffixcd,
        nullif(trim(RECIPIENTNAMEFIRST), '')                           as recipientnamefirst,
        nullif(trim(RECIPIENTNAMEPREFIXCD), '')                        as recipientnameprefixcd,
        nullif(trim(RECIPIENTNAMESHORT), '')                           as recipientnameshort,
        nullif(trim(BENEFICIARYPERSENTTYPECD), '')                     as beneficiarypersenttypecd,
        nullif(trim(BENEFICIARYNAMEORGANIZATION), '')                  as beneficiarynameorganization,
        nullif(trim(BENEFICIARYNAMELAST), '')                          as beneficiarynamelast,
        nullif(trim(BENEFICIARYNAMESUFFIXCD), '')                      as beneficiarynamesuffixcd,
        nullif(trim(BENEFICIARYNAMEFIRST), '')                         as beneficiarynamefirst,
        nullif(trim(BENEFICIARYNAMEPREFIXCD), '')                      as beneficiarynameprefixcd,
        nullif(trim(BENEFICIARYNAMESHORT), '')                         as beneficiarynameshort,
        to_timestamp_ntz(INGESTED_AT, 6)                               as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                                as _source_run_id
    from source
)

select * from renamed
