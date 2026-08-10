{{ config(materialized='view') }}

/*
  Generated 2026-08-09 (73-source backlog, wave 2b) from live-verified specs.
  Texas lobby transportation/lodging expenditures: one row per travel line (lobactivitytravelid unique; lobbyactivityid repeats across legs).
  Grain: one row = one travel line.
*/

with source as (
    select * from {{ source('ripple_raw', 'TX_LOBBY_TRANSPORTATION') }}
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
        nullif(trim(LOBACTIVITYTRAVELID), '')                          as travel_id,
        nullif(trim(CREDITCARDFLAG), '')                               as creditcardflag,
        nullif(trim(LOBBYACTIVITYPERIODCD), '')                        as lobbyactivityperiodcd,
        nullif(trim(RECIPIENTPERSENTTYPECD), '')                       as recipientpersenttypecd,
        nullif(trim(RECIPIENTNAMEORGANIZATION), '')                    as recipientnameorganization,
        nullif(trim(RECIPIENTNAMELAST), '')                            as recipientnamelast,
        nullif(trim(RECIPIENTNAMESUFFIXCD), '')                        as recipientnamesuffixcd,
        nullif(trim(RECIPIENTNAMEFIRST), '')                           as recipientnamefirst,
        nullif(trim(RECIPIENTNAMEPREFIXCD), '')                        as recipientnameprefixcd,
        nullif(trim(RECIPIENTNAMESHORT), '')                           as recipientnameshort,
        nullif(trim(LODGINGNAME), '')                                  as lodgingname,
        nullif(trim(LODGINGSTREETADDR1), '')                           as lodgingstreetaddr1,
        nullif(trim(LODGINGSTREETADDR2), '')                           as lodgingstreetaddr2,
        nullif(trim(LODGINGSTREETCITY), '')                            as lodgingstreetcity,
        nullif(trim(LODGINGSTREETSTATECD), '')                         as lodgingstreetstatecd,
        nullif(trim(LODGINGSTREETCOUNTRYCD), '')                       as lodgingstreetcountrycd,
        nullif(trim(LODGINGSTREETPOSTALCODE), '')                      as lodgingstreetpostalcode,
        nullif(trim(LODGINGSTREETREGION), '')                          as lodgingstreetregion,
        try_to_date(nullif(trim(CHECKINDT), ''), 'YYYYMMDD')           as checkindt,
        try_to_date(nullif(trim(CHECKOUTDT), ''), 'YYYYMMDD')          as checkoutdt,
        nullif(trim(TRANSPORTATIONTYPECD), '')                         as transportationtypecd,
        nullif(trim(TRANSPORTATIONTYPEDESCR), '')                      as transportationtypedescr,
        nullif(trim(DEPARTURECITY), '')                                as departurecity,
        try_to_date(nullif(trim(DEPARTUREDT), ''), 'YYYYMMDD')         as departuredt,
        nullif(trim(ARRIVALCITY), '')                                  as arrivalcity,
        try_to_date(nullif(trim(ARRIVALDT), ''), 'YYYYMMDD')           as arrivaldt,
        nullif(trim(TRAVELPURPOSE), '')                                as travelpurpose,
        to_timestamp_ntz(INGESTED_AT, 6)                               as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                                as _source_run_id
    from source
)

select * from renamed
