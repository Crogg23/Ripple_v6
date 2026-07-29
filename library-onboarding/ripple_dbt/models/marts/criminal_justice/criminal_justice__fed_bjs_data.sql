{{ config(materialized='table', schema='CRIMINAL_JUSTICE') }}

-- GRAIN: one row per victimization incident (NCVS survey)

with source as (
    select * from {{ source('ripple_raw', 'FED_BJS_DATA') }}
)

select
    IDPER,
    YEARQ,
    "YEAR" as YEAR,
    AGER,
    SEX,
    HISPANIC,
    RACE,
    RACE_ETHNICITY,
    HINCOME1,
    HINCOME2,
    MARITAL,
    POPSIZE,
    REGION,
    MSA,
    LOCALITY,
    EDUCATN1,
    EDUCATN2,
    VETERAN,
    CITIZEN,
    NEWCRIME,
    NEWOFF,
    SERIOUSVIOLENT,
    NOTIFY,
    VICSERVICES,
    LOCATIONR,
    DIREL,
    WEAPON,
    WEAPCAT,
    INJURY,
    SERIOUS,
    TREATMENT,
    OFFENDERAGE,
    OFFENDERSEX,
    OFFTRACENEW,
    WGTVICCY,
    SERIES,
    NEWWGT
from source
