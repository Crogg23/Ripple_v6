{{ config(materialized='table', schema='REFERENCE') }}

-- GRAIN: one row per FIPS county code (~3,200 US counties)
-- Answers: What county/state does a FIPS code map to, and what's its centroid?
-- Source: Derived from EPA FRS facilities (richest FIPS coverage in the warehouse)
-- Key joins: fips_code used by EPA ECHO, Vera, MSHA, MEDSL elections, CDC data

with frs_geo as (
    select
        trim("FIPS_CODE")                              as fips_code,
        trim("COUNTY_NAME")                            as county_name,
        trim("STATE_CODE")                             as state_abbr,
        trim("STATE_NAME")                             as state_name,
        trim("EPA_REGION_CODE")                        as epa_region,
        trim("CONGRESSIONAL_DIST_NUM")                 as congressional_district,
        try_to_double("LATITUDE83")                    as latitude,
        try_to_double("LONGITUDE83")                   as longitude
    from {{ source('ripple_raw', 'FED_EPA_FRS_FULL') }}
    where trim("FIPS_CODE") is not null
      and trim("FIPS_CODE") != ''
      and try_to_double("LATITUDE83") is not null
),

aggregated as (
    select
        fips_code,
        any_value(county_name)                         as county_name,
        any_value(state_abbr)                          as state_abbr,
        any_value(state_name)                          as state_name,
        any_value(epa_region)                          as epa_region,
        round(avg(latitude), 5)                        as centroid_latitude,
        round(avg(longitude), 5)                       as centroid_longitude,
        count(*)                                       as facility_count
    from frs_geo
    group by fips_code
)

select
    fips_code,
    left(fips_code, 2)                                 as state_fips,
    right(fips_code, 3)                                as county_fips_suffix,
    county_name,
    state_abbr,
    state_name,
    epa_region,
    centroid_latitude,
    centroid_longitude,
    facility_count
from aggregated
