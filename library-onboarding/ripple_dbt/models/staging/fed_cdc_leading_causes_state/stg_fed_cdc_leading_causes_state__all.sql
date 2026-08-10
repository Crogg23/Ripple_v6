{{ config(materialized='view') }}

/*
  Hand-built 2026-08-09 for the dead-source rebuild sprint (fed_cdc_leading_causes_state).
  Grain: one row = one state (incl. 'United States' rollup) x year x leading
  cause of death, 1999-2017; (year, state, cause_name) verified unique
  (10,868 = 10,868). This is the state-geography companion to the CDC WONDER
  national grid (WONDER's API is national-only by CDC policy).
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_CDC_LEADING_CAUSES_STATE') }}
),

renamed as (
    select
        try_to_number(trim(YEAR))                                         as year,
        nullif(trim(STATE), '')                                           as state,
        nullif(trim(CAUSE_NAME), '')                                      as cause_name,
        nullif(trim(C_113_CAUSE_NAME), '')                                as icd_113_cause_name,
        try_to_number(replace(trim(DEATHS), ',', ''))                     as deaths,
        try_to_double(replace(trim(AGE_ADJUSTED_DEATH_RATE), ',', ''))    as age_adjusted_death_rate,
        to_timestamp_ntz(_INGESTED_AT, 6)                                 as _ingested_at,
        nullif(trim(_SOURCE_RUN_ID), '')                                  as _source_run_id
    from source
)

select * from renamed
