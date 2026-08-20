{{ config(materialized='table', schema='CONSUMER_SAFETY') }}

-- GRAIN: one row per injury case (cpsc_case_number is unique)
-- Answers: What consumer products cause injuries, how severe, to whom?
-- Source: CPSC NEISS (National Electronic Injury Surveillance System) â€” ~9.8M cases
-- Key joins: product_1/2/3 â†’ CPSC product codes; body_part/diagnosis â†’ NEISS code lookups

with source as (
    select * from {{ source('ripple_raw', 'FED_CPSC_NEISS') }}
)

select
    trim("CPSC_CASE_NUMBER")                        as case_number,
    try_to_date(trim("TREATMENT_DATE"), 'MM/DD/YYYY') as treatment_date,
    try_to_number("_SRC_YEAR")                      as data_year,
    try_to_number("AGE")                            as age,
    trim("SEX")                                     as sex_code,
    trim("RACE")                                    as race_code,
    trim("HISPANIC")                                as hispanic_code,
    trim("BODY_PART")                               as body_part_code,
    trim("DIAGNOSIS")                               as diagnosis_code,
    trim("DISPOSITION")                             as disposition_code,
    trim("LOCATION")                                as location_code,
    trim("FIRE_INVOLVEMENT")                        as fire_involvement,
    trim("PRODUCT_1")                               as product_code_1,
    trim("PRODUCT_2")                               as product_code_2,
    trim("PRODUCT_3")                               as product_code_3,
    trim("ALCOHOL")                                 as alcohol_involved,
    trim("DRUG")                                    as drug_involved,
    "NARRATIVE"                                     as narrative,
    trim("STRATUM")                                 as stratum,
    try_to_double("WEIGHT")                         as statistical_weight,
    -- RECOVERED 2026-08-20 (time-index scan): the LOADER wrote this stamp
    -- already broken -- all 9,794,971 rows land in the year 56,569,708 because
    -- microseconds were cast as seconds before the row ever reached dbt. The
    -- original is exactly recoverable (verified: recovers to 2026-07-26).
    {{ ripple_recover_ingest_ts('"_INGESTED_AT"') }} as _loaded_at,
    "_SOURCE_RUN_ID" as _source_run_id
from source
qualify row_number() over (
    partition by "CPSC_CASE_NUMBER"
    order by "_INGESTED_AT" desc
) = 1
