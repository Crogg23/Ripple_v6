{{ config(materialized='view') }}

/*
  Generated 2026-08-09 (73-source backlog, wave 2c) from live-verified specs.
  PBGC trusteed single-employer pension plans (failed plans taken over by the federal insurer): one row per case (case_number unique) with sponsor, EIN, termination/trusteeship dates, participant count.
  Grain: one row = one trusteed plan case.
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_PBGC_TRUSTEED_PLANS') }}
),

renamed as (
    select
        nullif(trim(CASE_NUMBER), '')                              as case_number,
        nullif(trim(SPONSOR_NAME), '')                             as sponsor_name,
        nullif(trim(PLAN_NAME), '')                                as plan_name,
        nullif(trim(EIN), '')                                      as ein,
        nullif(trim(PLAN_NUMBER), '')                              as plan_number,
        nullif(trim(CITY), '')                                     as city,
        nullif(trim(STATE), '')                                    as state,
        try_to_date(left(nullif(trim(DATE_OF_PLAN_TERMINATION), ''), 10)) as date_of_plan_termination,
        try_to_date(left(nullif(trim(DATE_OF_PBGC_TRUSTEESHIP), ''), 10)) as date_of_pbgc_trusteeship,
        try_to_number(nullif(trim(NUMBER_OF_PARICIPANTS_AT_DATE_OF_PLAN_TERMINATION), ''), 18, 4) as number_of_paricipants_at_date_of_plan_termination,
        to_timestamp_ntz(INGESTED_AT, 6)                           as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                            as _source_run_id
    from source
)

select * from renamed
