{{ config(materialized='table', schema='CONSUMER_SAFETY') }}

-- GRAIN: one row per complaint (cmplid is unique)
-- Answers: What vehicles are generating safety complaints, and how much harm?
-- Source: NHTSA ODI Consumer Complaints (~2.2M since 1995)
-- Key joins: mfr_name â†’ manufacturer entities; state â†’ geography

select
    cmplid,
    odino,
    mfr_name,
    maketxt                              as make,
    modeltxt                             as model,
    yeartxt                              as model_year,
    compdesc                             as component,
    crash,
    fire,
    injured,
    deaths,
    fail_date,
    date_received,
    miles,
    occurrences,
    cmpl_type,
    city,
    state,
    vin,
    prod_type,
    cdescr                               as complaint_description,
    medical_attn,
    vehicles_towed_yn                    as vehicle_towed,
    (crash = 'Y')                        as involved_crash,
    (fire = 'Y')                         as involved_fire,
    (deaths > 0)                         as is_fatal,
    (injured > 0 or deaths > 0)          as caused_harm,
    _loaded_at,
    _source_run_id
from {{ ref('stg_fed_nhtsa_complaints__records') }}
