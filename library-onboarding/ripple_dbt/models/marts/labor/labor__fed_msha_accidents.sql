{{ config(materialized='table', schema='LABOR') }}

-- GRAIN: one row per accident document (document_no is unique)
-- Answers: What mining accidents occurred, where, severity, and who was responsible?
-- Source: MSHA Accidents (~274K records)
-- Key joins: mine_id → msha_mines/violations; fips_state_cd → geography

select
    document_no,
    mine_id,
    controller_id,
    controller_name,
    operator_id,
    operator_name,
    subunit,
    try_to_date(accident_dt, 'YYYYMMDD')           as accident_date,
    try_to_number(cal_yr)                          as cal_yr,
    degree_injury_cd,
    degree_injury,
    fips_state_cd,
    classification,
    accident_type,
    try_to_number(no_injuries)                     as no_injuries,
    try_to_number(days_lost)                       as days_lost,
    try_to_number(days_restrict)                   as days_restrict,
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
qualify row_number() over (partition by document_no order by _loaded_at desc) = 1
