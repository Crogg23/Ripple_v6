{{ config(materialized='table', schema='ENVIRONMENT') }}

-- GRAIN: one row per EPA-registered facility (REGISTRY_ID is unique)
-- Answers: Where is every EPA-regulated facility in the US, who runs it, what programs cover it?
-- Source: EPA Facility Registry Service (~5.3M facilities)
-- Key joins: fips_code â†’ geography; primary_name â†’ entity resolution; pgm_sys_acrnms â†’ EPA program tables

with source as (
    select * from {{ source('ripple_raw', 'FED_EPA_FRS_FULL') }}
)

select
    trim("REGISTRY_ID")                             as registry_id,
    trim("PRIMARY_NAME")                            as facility_name,
    trim("LOCATION_ADDRESS")                        as address,
    trim("SUPPLEMENTAL_LOCATION")                   as supplemental_location,
    trim("CITY_NAME")                               as city,
    trim("COUNTY_NAME")                             as county,
    trim("FIPS_CODE")                               as fips_code,
    trim("STATE_CODE")                              as state_code,
    trim("STATE_NAME")                              as state_name,
    trim("POSTAL_CODE")                             as postal_code,
    trim("CONGRESSIONAL_DIST_NUM")                  as congressional_district,
    trim("EPA_REGION_CODE")                         as epa_region,
    trim("SITE_TYPE_NAME")                          as site_type,
    trim("FEDERAL_FACILITY_CODE")                   as federal_facility_code,
    trim("FEDERAL_AGENCY_NAME")                     as federal_agency,
    trim("TRIBAL_LAND_CODE")                        as tribal_land_code,
    trim("TRIBAL_LAND_NAME")                        as tribal_land_name,
    try_to_double("LATITUDE83")                     as latitude,
    try_to_double("LONGITUDE83")                    as longitude,
    trim("PGM_SYS_ACRNMS")                         as program_system_acronyms,
    -- FIXED 2026-08-20 (time-index scan): EPA ships these as DD-MON-YY with a
    -- TWO-DIGIT year ('01-MAR-00', '02-JUN-16', '25-SEP-25'). A bare try_to_date
    -- read the year literally, landing all 5,300,149 create dates and 2,782,106
    -- update dates in years 0000-0026. Verified against the raw landing table.
    -- Pivot 2069: EPA's registry postdates 1990, so every 2-digit year is 20xx.
    {{ ripple_ts_from_date('"CREATE_DATE"', 'dmon2', 2069) }}::date as create_date,
    {{ ripple_ts_from_date('"UPDATE_DATE"', 'dmon2', 2069) }}::date as update_date,
    (trim("FEDERAL_FACILITY_CODE") = 'Y') as is_federal_facility,
    (trim("TRIBAL_LAND_CODE") = 'Y') as is_on_tribal_land,
    "_INGESTED_AT" as _loaded_at,
    "_SOURCE_RUN_ID" as _source_run_id
from source
qualify row_number() over (
    partition by "REGISTRY_ID"
    order by "_INGESTED_AT" desc
) = 1
