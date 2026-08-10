{{ config(materialized='view') }}

/*
  Generated 2026-08-09 (73-source backlog, wave 2b) from live-verified specs.
  Texas lobby food & beverage expenditures on state officials: one row per activity (lobbyactivityid unique).
  Grain: one row = one food/beverage activity.
*/

with source as (
    select * from {{ source('ripple_raw', 'TX_LOBBY_FOOD_BEVERAGE') }}
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
        nullif(trim(ACTIVITYAMOUNTCD), '')                             as activityamountcd,
        try_to_number(nullif(trim(ACTIVITYEXACTAMOUNT), ''), 18, 2)    as activityexactamount,
        try_to_number(nullif(trim(ACTIVITYAMOUNTRANGELOW), ''), 18, 2) as activityamountrangelow,
        try_to_number(nullif(trim(ACTIVITYAMOUNTRANGEHIGH), ''), 18, 2) as activityamountrangehigh,
        nullif(trim(RECIPIENTPERSENTTYPECD), '')                       as recipientpersenttypecd,
        nullif(trim(RECIPIENTNAMEORGANIZATION), '')                    as recipientnameorganization,
        nullif(trim(RECIPIENTNAMELAST), '')                            as recipientnamelast,
        nullif(trim(RECIPIENTNAMESUFFIXCD), '')                        as recipientnamesuffixcd,
        nullif(trim(RECIPIENTNAMEFIRST), '')                           as recipientnamefirst,
        nullif(trim(RECIPIENTNAMEPREFIXCD), '')                        as recipientnameprefixcd,
        nullif(trim(RECIPIENTNAMESHORT), '')                           as recipientnameshort,
        nullif(trim(RESTAURANTNAME), '')                               as restaurantname,
        nullif(trim(RESTAURANTSTREETCITY), '')                         as restaurantstreetcity,
        nullif(trim(RESTAURANTSTREETSTATECD), '')                      as restaurantstreetstatecd,
        nullif(trim(RESTAURANTSTREETCOUNTRYCD), '')                    as restaurantstreetcountrycd,
        nullif(trim(RESTAURANTSTREETPOSTALCODE), '')                   as restaurantstreetpostalcode,
        nullif(trim(RESTAURANTSTREETREGION), '')                       as restaurantstreetregion,
        to_timestamp_ntz(INGESTED_AT, 6)                               as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                                as _source_run_id
    from source
)

select * from renamed
