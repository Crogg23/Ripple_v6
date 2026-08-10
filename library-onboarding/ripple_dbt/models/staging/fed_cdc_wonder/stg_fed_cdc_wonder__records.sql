{{ config(materialized='view') }}

/*
  Rewritten 2026-08-09: the 2026-08-09 rebuild replaced the old landing shape
  (DATABASE_ID / GROUP_BY_n XML capture) with a tidy national year x ICD chapter
  x sex mortality grid from the live WONDER API (which is national-only by CDC
  policy — state grouping is rejected; see fed_cdc_leading_causes_state for
  state geography). (year, icd_chapter, sex) verified unique (880 = 880).
  Counts carry thousands separators — stripped before casting.
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_CDC_WONDER') }}
),

renamed as (
    select
        try_to_number(trim(YEAR))                                         as year,
        nullif(trim(ICD_CHAPTER), '')                                     as icd_chapter,
        nullif(trim(SEX), '')                                             as sex,
        try_to_number(replace(trim(DEATHS), ',', ''))                     as deaths,
        try_to_number(replace(trim(POPULATION), ',', ''))                 as population,
        try_to_double(replace(trim(CRUDE_RATE), ',', ''))                 as crude_rate,
        to_timestamp_ntz(_INGESTED_AT, 6)                                 as _ingested_at,
        nullif(trim(_SOURCE_RUN_ID), '')                                  as _source_run_id
    from source
)

select * from renamed
