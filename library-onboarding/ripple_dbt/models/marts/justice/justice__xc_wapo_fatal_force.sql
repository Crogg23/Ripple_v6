{{ config(materialized='table', schema='JUSTICE') }}

-- GRAIN: one row per fatal encounter (id is unique)
-- Answers: Who is killed by police, where, and under what circumstances?
-- Source: Washington Post Fatal Force Database
-- Key joins: state â†’ geography; race + age + gender â†’ demographics

with base as (
    select * from {{ ref('stg_xc_wapo_fatal_force__records') }}
)

select
    id,
    trim(name)                                   as victim_name,
    try_to_number(age)                           as age,
    trim(gender)                                 as gender,
    trim(race)                                   as race,
    try_to_date(date, 'YYYY-MM-DD')              as incident_date,
    trim(city)                                   as city,
    trim(county)                                 as county,
    trim(state)                                  as state,
    try_to_double(latitude)                      as latitude,
    try_to_double(longitude)                     as longitude,
    trim(threat_type)                            as threat_type,
    trim(flee_status)                            as flee_status,
    trim(armed_with)                             as armed_with,
    (trim(was_mental_illness_related) = 'True')  as mental_illness_related,
    (trim(body_camera) = 'True')                 as body_camera_present,
    trim(race_source)                            as race_source,
    _loaded_at
from base
