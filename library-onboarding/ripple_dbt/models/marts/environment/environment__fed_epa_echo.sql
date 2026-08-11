{{ config(materialized='table', schema='ENVIRONMENT') }}

-- GRAIN: one row per EPA-regulated facility (FRS_ID is unique)
-- Answers: Which facilities violate environmental law, how much are they penalized,
--   and what are the demographics of surrounding communities?
-- Source: EPA ECHO (Enforcement and Compliance History Online) â€” ~3.2M facilities
-- COUNT vs PUBLISHER (verified 2026-08-11): we hold 3.14M distinct facility ids, rows unique -- NOT a double-load. EPA's "more than 1.5 million regulated facilities" is soft ad copy, not an exact corpus count.
-- Key joins: frs_id â†’ epa_frs; fac_fips_code â†’ geography; fac_name â†’ entity resolution

with source as (
    select * from {{ source('ripple_raw', 'FED_EPA_ECHO') }}
)

select
    trim("FRS_ID")                                    as frs_id,
    trim("FAC_NAME")                                  as facility_name,
    trim("FAC_STREET")                                as street,
    trim("FAC_CITY")                                  as city,
    trim("FAC_STATE")                                 as state,
    trim("FAC_ZIP")                                   as zip,
    trim("FAC_COUNTY")                                as county,
    trim("FAC_FIPS_CODE")                             as fips_code,
    trim("FAC_EPA_REGION")                            as epa_region,
    try_to_double("FAC_LAT")                          as latitude,
    try_to_double("FAC_LONG")                         as longitude,
    try_to_double("FAC_PERCENT_MINORITY")             as pct_minority,
    try_to_double("FAC_POP_DEN")                      as population_density,

    -- Compliance summary
    trim("FAC_COMPLIANCE_STATUS")                     as compliance_status,
    trim("FAC_SNC_FLG")                               as significant_noncompliance_flag,
    try_to_number("FAC_QTRS_WITH_NC")                 as quarters_with_noncompliance,
    trim("FAC_3YR_COMPLIANCE_HISTORY")                as three_yr_compliance_history,

    -- Inspections
    try_to_number("FAC_INSPECTION_COUNT")             as total_inspection_count,
    try_to_date(trim("FAC_DATE_LAST_INSPECTION"))     as date_last_inspection,
    try_to_number("FAC_DAYS_LAST_INSPECTION")         as days_since_last_inspection,

    -- Enforcement actions
    try_to_number("FAC_INFORMAL_COUNT")               as informal_action_count,
    try_to_number("FAC_FORMAL_ACTION_COUNT")          as formal_action_count,
    try_to_date(trim("FAC_DATE_LAST_FORMAL_ACTION"))  as date_last_formal_action,

    -- Penalties
    try_to_double("FAC_TOTAL_PENALTIES")              as total_penalties,
    try_to_number("FAC_PENALTY_COUNT")                as penalty_count,
    try_to_double("FAC_LAST_PENALTY_AMT")             as last_penalty_amt,
    try_to_date(trim("FAC_DATE_LAST_PENALTY"))        as date_last_penalty,

    -- Program flags
    (trim("AIR_FLAG") = 'Y') as has_air_program,
    (trim("NPDES_FLAG") = 'Y') as has_water_program,
    (trim("RCRA_FLAG") = 'Y') as has_hazwaste_program,
    (trim("SDWIS_FLAG") = 'Y') as has_drinking_water_program,
    (trim("TRI_FLAG") = 'Y') as has_toxic_release_program,
    (trim("GHG_FLAG") = 'Y') as has_greenhouse_gas_program,

    -- TRI releases
    try_to_double("TRI_RELEASES_TRANSFERS")           as tri_total_releases_transfers,
    try_to_double("TRI_ON_SITE_RELEASES")             as tri_on_site_releases,

    -- Facility flags
    (trim("FAC_MAJOR_FLAG") = 'Y') as is_major_facility,
    (trim("FAC_ACTIVE_FLAG") = 'Y') as is_active,
    (trim("FAC_FEDERAL_FLG") = 'Y') as is_federal_facility,
    (trim("FAC_INDIAN_CNTRY_FLG") = 'Y') as is_on_tribal_land,

    -- Derived: high-risk signal
    (try_to_number("FAC_QTRS_WITH_NC") >= 4
     and try_to_double("FAC_TOTAL_PENALTIES") < 1000) as penalty_gap_flag,

    "_INGESTED_AT" as _loaded_at,
    "_SOURCE_RUN_ID" as _source_run_id
from source
qualify row_number() over (
    partition by "FRS_ID"
    order by "_INGESTED_AT" desc
) = 1
