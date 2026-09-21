{{ config(materialized='view') }}

-- GRAIN: one row per NCVS person-level victimization record (survey microdata).
-- The landing table holds NCVS (National Crime Victimization Survey) microdata,
-- NOT a BJS data-collections catalog (earlier version of this model was wrong).
-- Rows are NOT unique on person id (idper) or any obvious key: a person can
-- report multiple victimizations, and weighted survey records can repeat.
-- Passthrough stage: rename, NULLIF-empty-string clean, guarded numeric casts.
--
-- Repointed 2026-09-20: FED_BJS_DATA was a page-capped landing pull (1,000
-- rows, live-confirmed). FED_BJS_DATA_FULL is the corrected full reload
-- (68,852 rows, live-confirmed 2026-09-20) and carries the identical 40-column
-- set (DESCRIBE TABLE compared column-for-column, same names/order) -- no
-- select-list changes needed, source() swap only.

with source as (

    select *
    from {{ source('ripple_raw', 'FED_BJS_DATA_FULL') }}

),

renamed as (

    select
        -- identifiers
        nullif(trim(IDPER), '')            as person_id,

        -- survey period
        nullif(trim(YEARQ), '')            as year_quarter,       -- e.g. '1993.1'
        {{ ripple_num('"YEAR"') }}         as survey_year,

        -- respondent demographics (coded values; negatives are NCVS sentinels)
        nullif(trim(AGER), '')             as age_group_code,
        nullif(trim(SEX), '')              as sex_code,
        nullif(trim(HISPANIC), '')         as hispanic_code,
        nullif(trim(RACE), '')             as race_code,
        nullif(trim(RACE_ETHNICITY), '')   as race_ethnicity_code,
        nullif(trim(HINCOME1), '')         as household_income_code_1,
        nullif(trim(HINCOME2), '')         as household_income_code_2,
        nullif(trim(MARITAL), '')          as marital_status_code,
        nullif(trim(EDUCATN1), '')         as education_code_1,
        nullif(trim(EDUCATN2), '')         as education_code_2,
        nullif(trim(VETERAN), '')          as veteran_code,
        nullif(trim(CITIZEN), '')          as citizen_code,

        -- geography / area
        nullif(trim(POPSIZE), '')          as population_size_code,
        nullif(trim(REGION), '')           as region_code,
        nullif(trim(MSA), '')              as msa_code,
        nullif(trim(LOCALITY), '')         as locality_code,

        -- victimization characteristics
        nullif(trim(NEWCRIME), '')         as crime_type_code,
        nullif(trim(NEWOFF), '')           as offense_code,
        nullif(trim(SERIOUSVIOLENT), '')   as serious_violent_code,
        nullif(trim(NOTIFY), '')           as police_notified_code,
        nullif(trim(VICSERVICES), '')      as victim_services_code,
        nullif(trim(LOCATIONR), '')        as location_code,
        nullif(trim(DIREL), '')            as victim_offender_relationship_code,
        nullif(trim(WEAPON), '')           as weapon_code,
        nullif(trim(WEAPCAT), '')          as weapon_category_code,
        nullif(trim(INJURY), '')           as injury_code,
        nullif(trim(SERIOUS), '')          as serious_injury_code,
        nullif(trim(TREATMENT), '')        as medical_treatment_code,

        -- offender characteristics
        nullif(trim(OFFENDERAGE), '')      as offender_age_code,
        nullif(trim(OFFENDERSEX), '')      as offender_sex_code,
        nullif(trim(OFFTRACENEW), '')      as offender_race_code,

        -- survey weights / series flag
        {{ ripple_num('WGTVICCY') }}       as victimization_weight,
        nullif(trim(SERIES), '')           as series_flag,
        {{ ripple_num('NEWWGT') }}         as adjusted_weight,

        -- pipeline metadata
        -- landing _INGESTED_AT is a TIMESTAMP that swallowed epoch micros as seconds (year 56 million); re-read the epoch
        {{ landing_parse_audit_epoch('date_part(epoch_second, _INGESTED_AT)') }} as _ingested_at,
        _SOURCE_RUN_ID                     as _source_run_id

    from source

)

select * from renamed
