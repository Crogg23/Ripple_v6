{{ config(materialized='table', schema='CRIMINAL_JUSTICE') }}

-- GRAIN: one row per NCVS person-level victimization record (survey microdata)

with staged as (
    select * from {{ ref('stg_fed_bjs_data__bjs_data_collections') }}
)

select
    person_id,
    year_quarter,
    survey_year,
    age_group_code,
    sex_code,
    hispanic_code,
    race_code,
    race_ethnicity_code,
    household_income_code_1,
    household_income_code_2,
    marital_status_code,
    population_size_code,
    region_code,
    msa_code,
    locality_code,
    education_code_1,
    education_code_2,
    veteran_code,
    citizen_code,
    crime_type_code,
    offense_code,
    serious_violent_code,
    police_notified_code,
    victim_services_code,
    location_code,
    victim_offender_relationship_code,
    weapon_code,
    weapon_category_code,
    injury_code,
    serious_injury_code,
    medical_treatment_code,
    offender_age_code,
    offender_sex_code,
    offender_race_code,
    victimization_weight,
    series_flag,
    adjusted_weight,
    _ingested_at,
    _source_run_id
from staged
