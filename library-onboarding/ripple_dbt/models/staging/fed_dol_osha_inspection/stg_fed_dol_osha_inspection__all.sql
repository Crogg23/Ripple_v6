{{ config(materialized='view', tags=['spine_generated']) }}

-- GRAIN: one row per inspection (ACTIVITY_NR is unique)
-- SPINE_ENTITY: organization (by ESTAB_NAME + SITE_ADDRESS)
-- Source: DOL OSHA — ~5.2M inspections back to 1970s
-- Key joins: NAICS/SIC → industry lookups; ESTAB_NAME → entity resolution
--
-- FIXED 2026-08-25: the source table this view pointed at
-- (LIBRARY_RAW.LANDING.FED_DOL_OSHA_INSPECTION, singular) was DROP TABLE'd
-- 2026-07-27 after a corrupt chunked write_pandas load (see git history on
-- this file for the original incident note). This staging view was left
-- enabled and pointing at the dead table on purpose so the break stayed
-- visible -- that is the break the census grid caught
-- (reports/census_grid_2026-08-12/fill/) and that the not_null/unique tests
-- on activity_nr kept failing on ("...does not exist or not authorized").
-- scripts/osha_inspections_api_load.py has since re-pulled the source under
-- a NEW table name, LIBRARY_RAW.LANDING.FED_DOL_OSHA_INSPECTIONS (plural --
-- not a rename of the old table, a fresh load), confirmed live via
-- INFORMATION_SCHEMA.COLUMNS with the same 39-column shape this model
-- already expected (plus _SRC_SHA256, not present on the old table, now
-- carried through as metadata below). That loader is still running as of
-- this fix, so row counts here will keep climbing -- expected, not a bug.
-- The downstream mart (labor__fed_dol_osha_inspection.sql) is still
-- config(enabled=false) from the old incident and was left untouched here;
-- re-enabling it is a separate call.

with source as (
    select * from {{ source('ripple_raw', 'FED_DOL_OSHA_INSPECTIONS') }}
),

renamed as (
    select
        trim("ACTIVITY_NR")                          as activity_nr,
        trim("REPORTING_ID")                         as reporting_id,
        trim("STATE_FLAG")                           as state_flag,
        trim("ESTAB_NAME")                           as estab_name,
        trim("SITE_ADDRESS")                         as site_address,
        trim("SITE_CITY")                            as site_city,
        trim("SITE_STATE")                           as site_state,
        trim("SITE_ZIP")                             as site_zip,
        trim("OWNER_TYPE")                           as owner_type,
        trim("OWNER_CODE")                           as owner_code,
        trim("ADV_NOTICE")                           as adv_notice,
        trim("SAFETY_HLTH")                          as safety_hlth,
        trim("SIC_CODE")                             as sic_code,
        trim("NAICS_CODE")                           as naics_code,
        trim("INSP_TYPE")                            as insp_type,
        trim("INSP_SCOPE")                           as insp_scope,
        trim("WHY_NO_INSP")                          as why_no_insp,
        trim("UNION_STATUS")                         as union_status,
        trim("SAFETY_MANUF")                         as safety_manuf,
        trim("SAFETY_CONST")                         as safety_const,
        trim("SAFETY_MARIT")                         as safety_marit,
        trim("HEALTH_MANUF")                         as health_manuf,
        trim("HEALTH_CONST")                         as health_const,
        trim("HEALTH_MARIT")                         as health_marit,
        trim("MIGRANT")                              as migrant,
        trim("MAIL_STREET")                          as mail_street,
        trim("MAIL_CITY")                            as mail_city,
        trim("MAIL_STATE")                           as mail_state,
        trim("MAIL_ZIP")                             as mail_zip,
        trim("HOST_EST_KEY")                         as host_est_key,
        try_to_number("NR_IN_ESTAB")                 as nr_in_estab,
        try_to_date("OPEN_DATE")                      as open_date,
        try_to_date("CASE_MOD_DATE")                  as case_mod_date,
        try_to_date("CLOSE_CONF_DATE")                as close_conf_date,
        try_to_date("CLOSE_CASE_DATE")                as close_case_date,
        try_to_date("LOAD_DT")                        as load_dt,
        "_INGESTED_AT"                               as _ingested_at,
        "_SOURCE_RUN_ID"                             as _source_run_id,
        "_SRC_SHA256"                                as _src_sha256
    from source
)

select * from renamed
qualify row_number() over (
    partition by activity_nr
    order by _ingested_at desc
) = 1
