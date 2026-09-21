{{ config(materialized='table', schema='LABOR') }}

-- GRAIN: one row per accident document (document_no is unique)
-- Answers: What mining accidents occurred, where, severity, and who was responsible?
-- Source: MSHA Accidents (~274K records)
-- Key joins: mine_id â†’ msha_mines/violations; fips_state_cd â†’ geography

select
    document_no,
    mine_id,
    controller_id,
    controller_name,
    operator_id,
    operator_name,
    subunit,
    try_to_date(accident_dt, 'MM/DD/YYYY')         as accident_date,
    {{ stg_int('cal_yr') }}                          as cal_yr,
    degree_injury_cd,
    degree_injury,
    fips_state_cd,
    classification,
    accident_type,
    {{ stg_int('no_injuries') }}                     as no_injuries,
    {{ stg_int('days_lost') }}                       as days_lost,
    {{ stg_int('days_restrict') }}                   as days_restrict,
    occupation,
    activity,
    injury_source,
    nature_injury,
    inj_body_part,
    narrative,
    coal_metal_ind,
    (degree_injury_cd = '01') as is_fatality,
    _loaded_at
from {{ ref('stg_fed_msha_accidents__records') }}
qualify row_number() over (partition by document_no order by _loaded_at desc,
             -- tie-breakers 2026-09-18: the row's own values, so the same row wins every run
             mine_id nulls last, controller_id nulls last, controller_name nulls last,
             operator_id nulls last, operator_name nulls last, subunit nulls last, accident_dt nulls last,
             cal_yr nulls last, degree_injury_cd nulls last, degree_injury nulls last,
             fips_state_cd nulls last, classification nulls last, accident_type nulls last,
             no_injuries nulls last, days_lost nulls last, days_restrict nulls last, occupation nulls last,
             activity nulls last, injury_source nulls last, nature_injury nulls last,
             inj_body_part nulls last, narrative nulls last, coal_metal_ind nulls last
) = 1
