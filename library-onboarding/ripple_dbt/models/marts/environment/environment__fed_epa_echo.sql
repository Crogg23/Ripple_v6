{{ config(materialized='table', schema='ENVIRONMENT') }}

-- GRAIN: one row per EPA-regulated facility (FRS_ID is unique)
-- Answers: Which facilities violate environmental law, how much are they penalized,
--   and what are the demographics of surrounding communities?
-- Source: EPA ECHO (Enforcement and Compliance History Online) â€” ~3.2M facilities
-- COUNT vs PUBLISHER (verified 2026-08-11): we hold 3.14M distinct facility ids, rows unique -- NOT a double-load. EPA's "more than 1.5 million regulated facilities" is soft ad copy, not an exact corpus count.
-- Key joins: frs_id â†’ epa_frs; fac_fips_code â†’ geography; fac_name â†’ entity resolution

with source as (
    select * from {{ source('ripple_raw', 'FED_EPA_ECHO') }}
),

facilities as (
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
    {{ stg_float('"FAC_LAT"') }}                          as latitude,
    {{ stg_float('"FAC_LONG"') }}                         as longitude,
    {{ stg_float('"FAC_PERCENT_MINORITY"') }}             as pct_minority,
    {{ stg_float('"FAC_POP_DEN"') }}                      as population_density,

    -- Compliance summary
    trim("FAC_COMPLIANCE_STATUS")                     as compliance_status,
    trim("FAC_SNC_FLG")                               as significant_noncompliance_flag,
    {{ stg_int('"FAC_QTRS_WITH_NC"') }}                 as quarters_with_noncompliance,
    trim("FAC_3YR_COMPLIANCE_HISTORY")                as three_yr_compliance_history,

    -- Inspections
    {{ stg_int('"FAC_INSPECTION_COUNT"') }}             as total_inspection_count,
    {{ stg_date('trim("FAC_DATE_LAST_INSPECTION")') }}     as date_last_inspection,
    {{ stg_int('"FAC_DAYS_LAST_INSPECTION"') }}         as days_since_last_inspection,

    -- Enforcement actions
    {{ stg_int('"FAC_INFORMAL_COUNT"') }}               as informal_action_count,
    {{ stg_int('"FAC_FORMAL_ACTION_COUNT"') }}          as formal_action_count,
    {{ stg_date('trim("FAC_DATE_LAST_FORMAL_ACTION")') }}  as date_last_formal_action,

    -- Penalties
    {{ stg_float('"FAC_TOTAL_PENALTIES"') }}              as total_penalties,
    {{ stg_int('"FAC_PENALTY_COUNT"') }}                as penalty_count,
    {{ stg_float('"FAC_LAST_PENALTY_AMT"') }}             as last_penalty_amt,
    {{ stg_date('trim("FAC_DATE_LAST_PENALTY")') }}        as date_last_penalty,

    -- Program flags
    (trim("AIR_FLAG") = 'Y') as has_air_program,
    (trim("NPDES_FLAG") = 'Y') as has_water_program,
    (trim("RCRA_FLAG") = 'Y') as has_hazwaste_program,
    (trim("SDWIS_FLAG") = 'Y') as has_drinking_water_program,
    (trim("TRI_FLAG") = 'Y') as has_toxic_release_program,
    (trim("GHG_FLAG") = 'Y') as has_greenhouse_gas_program,

    -- TRI releases
    {{ stg_float('"TRI_RELEASES_TRANSFERS"') }}           as tri_total_releases_transfers,
    {{ stg_float('"TRI_ON_SITE_RELEASES"') }}             as tri_on_site_releases,

    -- Facility flags
    (trim("FAC_MAJOR_FLAG") = 'Y') as is_major_facility,
    (trim("FAC_ACTIVE_FLAG") = 'Y') as is_active,
    (trim("FAC_FEDERAL_FLG") = 'Y') as is_federal_facility,
    (trim("FAC_INDIAN_CNTRY_FLG") = 'Y') as is_on_tribal_land,

    -- Derived: high-risk signal
    ({{ stg_int('"FAC_QTRS_WITH_NC"') }} >= 4
     and {{ stg_float('"FAC_TOTAL_PENALTIES"') }} < 1000) as penalty_gap_flag,

    "_INGESTED_AT" as _loaded_at,
    "_SOURCE_RUN_ID" as _source_run_id
from source
qualify row_number() over (
    partition by "FRS_ID"
    order by "_INGESTED_AT" desc,
             -- tie-breakers 2026-09-18: the row's own values, so the same row wins every run
             "FAC_NAME" nulls last, "FAC_STREET" nulls last, "FAC_CITY" nulls last, "FAC_STATE" nulls last,
             "FAC_ZIP" nulls last, "FAC_COUNTY" nulls last, "FAC_FIPS_CODE" nulls last,
             "FAC_EPA_REGION" nulls last, "FAC_LAT" nulls last, "FAC_LONG" nulls last,
             "FAC_PERCENT_MINORITY" nulls last, "FAC_POP_DEN" nulls last,
             "FAC_COMPLIANCE_STATUS" nulls last, "FAC_SNC_FLG" nulls last, "FAC_QTRS_WITH_NC" nulls last,
             "FAC_3YR_COMPLIANCE_HISTORY" nulls last, "FAC_INSPECTION_COUNT" nulls last,
             "FAC_DATE_LAST_INSPECTION" nulls last, "FAC_DAYS_LAST_INSPECTION" nulls last,
             "FAC_INFORMAL_COUNT" nulls last, "FAC_FORMAL_ACTION_COUNT" nulls last,
             "FAC_DATE_LAST_FORMAL_ACTION" nulls last, "FAC_TOTAL_PENALTIES" nulls last,
             "FAC_PENALTY_COUNT" nulls last, "FAC_LAST_PENALTY_AMT" nulls last,
             "FAC_DATE_LAST_PENALTY" nulls last, "AIR_FLAG" nulls last, "NPDES_FLAG" nulls last,
             "RCRA_FLAG" nulls last, "SDWIS_FLAG" nulls last, "TRI_FLAG" nulls last, "GHG_FLAG" nulls last,
             "TRI_RELEASES_TRANSFERS" nulls last, "TRI_ON_SITE_RELEASES" nulls last,
             "FAC_MAJOR_FLAG" nulls last, "FAC_ACTIVE_FLAG" nulls last, "FAC_FEDERAL_FLG" nulls last,
             "FAC_INDIAN_CNTRY_FLG" nulls last, "_SOURCE_RUN_ID" nulls last
) = 1
)

select
    facilities.*,

    -- last_penalty_amt is CASE-level, not facility-level (pattern sweep
    -- 2026-07-27, confirmed): ECHO's exporter stamps one settlement's total on
    -- every facility the case covered — e.g. $468,600 repeated on 652 Verizon
    -- cell-site rows, same date. Summing the raw column multiplies settlements
    -- by their facility count (mart-wide it implies $22.25B vs $10.9B of real
    -- facility-level TOTAL_PENALTIES). The _allocated column divides the amount
    -- evenly across facilities sharing the same amount + same penalty date (the
    -- same-case fingerprint), so facility sums recover each settlement once.
    -- Rows with no penalty date can't be fingerprinted and pass through raw —
    -- check last_penalty_shared_facility_n before trusting any aggregate.
    iff(last_penalty_amt is null or date_last_penalty is null,
        last_penalty_amt,
        last_penalty_amt / count(*) over (
            partition by last_penalty_amt, date_last_penalty))
                                                      as last_penalty_amt_allocated,
    count(*) over (
        partition by last_penalty_amt, date_last_penalty)
                                                      as last_penalty_shared_facility_n
from facilities
