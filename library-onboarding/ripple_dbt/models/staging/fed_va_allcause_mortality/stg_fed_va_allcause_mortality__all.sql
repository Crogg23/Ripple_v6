{{ config(materialized='view') }}

/*
  Hand-built 2026-08-09 for the dead-source rebuild sprint (fed_va_allcause_mortality).
  Grain: one row = one cohort x sex x year x cause of death (ranked leading
  causes plus 'All cause' and 'Not ranked' rollup rows, rank NULL for those);
  (year, cohort, sex, cause_of_death) verified unique (2,808 = 2,808).
  Counts carry thousands separators; suppressed cells are '.' — both handled by
  the replace + try_to_number pattern. YPLL = years of potential life lost;
  ypll_pct is the workbook's second YPLL column (share of total YPLL).
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_VA_ALLCAUSE_MORTALITY') }}
),

renamed as (
    select
        {{ stg_int('trim(YEAR)') }}                                         as year,
        nullif(trim(COHORT), '')                                          as cohort,
        nullif(trim(SEX), '')                                             as sex,
        nullif(trim(CAUSE_OF_DEATH), '')                                  as cause_of_death,
        {{ stg_int('trim(RANK)') }}                                         as rank,
        {{ stg_int("replace(trim(NUMBER), ',', '')") }}                     as deaths,
        {{ stg_float("replace(trim(PERCENT), ',', '')") }}                    as percent_of_deaths,
        {{ stg_float("replace(trim(UNADJUSTED_RATE), ',', '')") }}            as unadjusted_rate,
        {{ stg_float("replace(trim(AGE_ADJUSTED_RATE), ',', '')") }}          as age_adjusted_rate,
        {{ stg_float("replace(trim(CRUDE_RATE), ',', '')") }}                 as crude_rate,
        {{ stg_float("replace(trim(YPLL), ',', '')") }}                       as ypll,
        {{ stg_float("replace(trim(YPLL_2), ',', '')") }}                     as ypll_pct,
        to_timestamp_ntz(_INGESTED_AT, 6)                                 as _ingested_at,
        nullif(trim(_SOURCE_RUN_ID), '')                                  as _source_run_id
    from source
)

select * from renamed
