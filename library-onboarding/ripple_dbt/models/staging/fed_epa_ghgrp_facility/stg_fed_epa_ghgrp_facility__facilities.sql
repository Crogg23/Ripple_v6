{{ config(materialized='view') }}

/*
  Generated 2026-08-10 (backlog wave 4) from live-verified specs.
  EPA Greenhouse Gas Reporting Program facility registry: name, address,
  lat/long, NAICS, parent company, and the FRS_ID cross-dataset join key.
  Grain: one row = one facility x reporting year (FACILITY_ID + YEAR verified
  exactly unique).
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_EPA_GHGRP_FACILITY') }}
),

renamed as (
    select
        -- identifiers
        {{ dbt_utils.generate_surrogate_key(['FACILITY_ID', 'YEAR']) }}    as facility_year_id,
        try_to_number(trim(FACILITY_ID))                           as facility_id,
        try_to_number(trim(YEAR))                                  as reporting_year,
        nullif(trim(FRS_ID), '')                                   as frs_id,
        nullif(trim(EGGRT_FACILITY_ID), '')                        as eggrt_facility_id,
        nullif(trim(PROGRAM_SYS_ID), '')                           as program_sys_id,
        nullif(trim(PROGRAM_NAME), '')                             as program_name,
        nullif(trim(SUBMISSION_ID), '')                            as submission_id,
        nullif(trim(TRIBAL_LAND_ID), '')                           as tribal_land_id,

        -- facility profile
        nullif(trim(FACILITY_NAME), '')                            as facility_name,
        nullif(trim(PARENT_COMPANY), '')                           as parent_company,
        nullif(trim(NAICS_CODE), '')                               as naics_code,
        nullif(trim(REPORTED_INDUSTRY_TYPES), '')                  as reported_industry_types,
        nullif(trim(FACILITY_TYPES), '')                           as facility_types,
        nullif(trim(REPORTED_SUBPARTS), '')                        as reported_subparts,
        nullif(trim(REPORTING_STATUS), '')                         as reporting_status,
        nullif(trim(EMISSION_CLASSIFICATION_CODE), '')             as emission_classification_code,

        -- location
        nullif(trim(ADDRESS1), '')                                 as address1,
        ADDRESS2                                                   as address2,
        nullif(trim(CITY), '')                                     as city,
        nullif(trim(STATE), '')                                    as state,
        nullif(trim(STATE_NAME), '')                               as state_name,
        nullif(trim(ZIP), '')                                      as zip,
        nullif(trim(COUNTY), '')                                   as county,
        nullif(trim(COUNTY_FIPS), '')                              as county_fips,
        try_to_number(trim(LATITUDE), 18, 6)                       as latitude,
        try_to_number(trim(LONGITUDE), 18, 6)                      as longitude,

        -- program details
        nullif(trim(CEMS_USED), '')                                as cems_used,
        nullif(trim(CO2_CAPTURED), '')                             as co2_captured,
        nullif(trim(EMITTED_CO2_SUPPLIED), '')                     as emitted_co2_supplied,
        BAMM_USED_DESC                                             as bamm_used_desc,
        BAMM_APPROVED                                              as bamm_approved,
        nullif(trim(UU_RD_EXEMPT), '')                             as uu_rd_exempt,
        nullif(trim(PROCESS_STATIONARY_CML), '')                   as process_stationary_cml,
        nullif(trim(COMMENTS), '')                                 as comments,
        nullif(trim(RR_MRV_PLAN_URL), '')                          as rr_mrv_plan_url,
        nullif(trim(RR_MONITORING_PLAN_FILENAME), '')              as rr_monitoring_plan_filename,
        RR_MONITORING_PLAN                                         as rr_monitoring_plan,

        -- metadata
        _ingested_at,
        _source_run_id
    from source
)

select * from renamed
