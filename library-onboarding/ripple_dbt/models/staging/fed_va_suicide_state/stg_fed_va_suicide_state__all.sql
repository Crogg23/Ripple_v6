{{ config(materialized='view') }}

/*
  Hand-built 2026-08-09 for the dead-source rebuild sprint (fed_va_suicide_state).
  Grain: one row = one record from one of four stacked appendix sheets
  ('Veteran Suicides by State', 'Veteran Suicides by Sex', 'Suicides by Age',
  'Suicides by Method'); the sheet column says which dimensions are populated.
  Full 9-column natural key (sheet + every dimension) verified unique
  (19,704 = 19,704). Suppressed cells null out via try_to_number/try_to_double.
  The by-sex/age/method sheets use YEAR; the by-state sheet uses YEAR_OF_DEATH —
  year_of_death coalesces both so every row has a year.
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_VA_SUICIDE_STATE') }}
),

renamed as (
    select
        nullif(trim(SHEET), '')                                           as sheet,
        coalesce(try_to_number(trim(YEAR_OF_DEATH)),
                 try_to_number(trim(YEAR)))                               as year_of_death,
        nullif(trim(GEOGRAPHIC_REGION), '')                               as geographic_region,
        nullif(trim(STATE), '')                                           as state,
        nullif(trim(SEX), '')                                             as sex,
        nullif(trim(AGE_GROUP), '')                                       as age_group,
        nullif(trim(GROUP_METHOD), '')                                    as group_method,
        nullif(trim(METHOD), '')                                          as method,
        try_to_number(trim(VETERAN_SUICIDES))                             as veteran_suicides,
        try_to_number(trim(POPULATION_ESTIMATE))                          as population_estimate,
        try_to_double(trim(VETERAN_SUICIDE_RATE_PER_100_000))             as veteran_suicide_rate_per_100k,
        try_to_number(trim(GENERAL_POPULATION_SUICIDES))                  as general_population_suicides,
        try_to_double(trim(GENERAL_POPULATION_RATE_PER_100_000))          as general_population_rate_per_100k,
        try_to_number(trim(SUICIDES))                                     as suicides,
        try_to_double(trim(GROUP_PERCENTAGE))                             as group_percentage,
        to_timestamp_ntz(_INGESTED_AT, 6)                                 as _ingested_at,
        nullif(trim(_SOURCE_RUN_ID), '')                                  as _source_run_id
    from source
)

select * from renamed
