{{ config(materialized='view') }}

/*
  Generated 2026-08-09 (73-source backlog, wave 2b) from live-verified specs.
  CAL-ACCESS lobbyist employer session totals: one row per employer per legislative session (4 published doubles in the 1999 session -- no unique test).
  Grain: one row = one employer-session.
*/

with source as (
    select * from {{ source('ripple_raw', 'CA_LOBBY_EMPLOYER') }}
),

renamed as (
    select
        nullif(trim(EMPLOYER_ID), '')                                  as employer_id,
        nullif(trim(SESSION_ID), '')                                   as session_id,
        nullif(trim(EMPLOYER_NAME), '')                                as employer_name,
        try_to_number(nullif(trim(CURRENT_QTR_AMT), ''), 18, 2)        as current_qtr_amt,
        try_to_number(nullif(trim(SESSION_TOTAL_AMT), ''), 18, 2)      as session_total_amt,
        nullif(trim(CONTRIBUTOR_ID), '')                               as contributor_id,
        nullif(trim(INTEREST_CD), '')                                  as interest_cd,
        nullif(trim(INTEREST_NAME), '')                                as interest_name,
        nullif(trim(SESSION_YR_1), '')                                 as session_yr_1,
        nullif(trim(SESSION_YR_2), '')                                 as session_yr_2,
        try_to_number(nullif(trim(YR_1_YTD_AMT), ''), 18, 2)           as yr_1_ytd_amt,
        try_to_number(nullif(trim(YR_2_YTD_AMT), ''), 18, 2)           as yr_2_ytd_amt,
        try_to_number(nullif(trim(QTR_1), ''), 18, 2)                  as qtr_1,
        try_to_number(nullif(trim(QTR_2), ''), 18, 2)                  as qtr_2,
        try_to_number(nullif(trim(QTR_3), ''), 18, 2)                  as qtr_3,
        try_to_number(nullif(trim(QTR_4), ''), 18, 2)                  as qtr_4,
        try_to_number(nullif(trim(QTR_5), ''), 18, 2)                  as qtr_5,
        try_to_number(nullif(trim(QTR_6), ''), 18, 2)                  as qtr_6,
        try_to_number(nullif(trim(QTR_7), ''), 18, 2)                  as qtr_7,
        try_to_number(nullif(trim(QTR_8), ''), 18, 2)                  as qtr_8,
        to_timestamp_ntz(INGESTED_AT, 6)                               as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                                as _source_run_id
    from source
)

select * from renamed
