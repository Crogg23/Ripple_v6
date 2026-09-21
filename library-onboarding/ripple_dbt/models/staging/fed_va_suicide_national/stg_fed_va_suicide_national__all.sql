{{ config(materialized='view') }}

/*
  Hand-built 2026-08-09 for the dead-source rebuild sprint (fed_va_suicide_national).
  Grain: one row = one cohort x year (x optional age group) of national suicide
  counts/rates; (year_of_death, cohort, age_group) verified unique (690 = 690)
  after the same-day parser fix that had been landing the by-age sub-tables
  column-shifted. Rows with age_group NULL are the full-cohort table (they carry
  the age-adjusted rates); rows with age_group set come from the stacked by-age
  sub-table (no age-adjusted rates published). FEMALE_AGE_GROUP is a workbook
  duplicate of AGE_GROUP and is dropped. Suppressed cells ('.') null out via
  try_to_number/try_to_double.
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_VA_SUICIDE_NATIONAL') }}
),

renamed as (
    select
        {{ stg_int('trim(YEAR_OF_DEATH)') }}                                as year_of_death,
        nullif(trim(COHORT), '')                                          as cohort,
        nullif(trim(AGE_GROUP), '')                                       as age_group,
        {{ stg_int('trim(SUICIDE_DEATHS)') }}                               as suicide_deaths,
        {{ stg_int('trim(POPULATION_ESTIMATE)') }}                          as population_estimate,
        {{ stg_float('trim(UNADJUSTED_RATE_PER_100_000)') }}                  as unadjusted_rate_per_100k,
        {{ stg_float('trim(AGE_ADJUSTED_RATE_PER_100_000)') }}                as age_adjusted_rate_per_100k,
        {{ stg_int('trim(MALE_SUICIDE_DEATHS)') }}                          as male_suicide_deaths,
        {{ stg_int('trim(MALE_POPULATION_ESTIMATE)') }}                     as male_population_estimate,
        {{ stg_float('trim(MALE_UNADJUSTED_RATE_PER_100_000)') }}             as male_unadjusted_rate_per_100k,
        {{ stg_float('trim(MALE_AGE_ADJUSTED_RATE_PER_100_000)') }}           as male_age_adjusted_rate_per_100k,
        {{ stg_int('trim(FEMALE_SUICIDE_DEATHS)') }}                        as female_suicide_deaths,
        {{ stg_int('trim(FEMALE_POPULATION_ESTIMATE)') }}                   as female_population_estimate,
        {{ stg_float('trim(FEMALE_UNADJUSTED_RATE_PER_100_000)') }}           as female_unadjusted_rate_per_100k,
        {{ stg_float('trim(FEMALE_AGE_ADJUSTED_RATE_PER_100_000)') }}         as female_age_adjusted_rate_per_100k,
        to_timestamp_ntz(_INGESTED_AT, 6)                                 as _ingested_at,
        nullif(trim(_SOURCE_RUN_ID), '')                                  as _source_run_id
    from source
)

select * from renamed
