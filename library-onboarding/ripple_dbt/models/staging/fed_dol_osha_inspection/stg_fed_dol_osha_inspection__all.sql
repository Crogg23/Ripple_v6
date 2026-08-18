{{ config(materialized='view', tags=['spine_generated']) }}

-- GRAIN: one row per inspection (ACTIVITY_NR is unique)
-- SPINE_ENTITY: organization (by ESTAB_NAME + SITE_ADDRESS)
-- Source: DOL OSHA — ~5.2M inspections back to 1970s
-- Key joins: NAICS/SIC → industry lookups; ESTAB_NAME → entity resolution
--
-- ⚠ BROKEN 2026-08-18: source table LIBRARY_RAW.LANDING.FED_DOL_OSHA_INSPECTION
-- DOES NOT EXIST. It is not a rename/re-pull -- checked every schema in
-- LIBRARY_RAW (EPSTEIN, LANDING, PUBLIC, RETIRED) for any OSHA inspection/
-- enforcement/citation table under any name; nothing exists except the
-- unrelated FED_OSHA_ITA_* self-reported-injury tables (a different OSHA
-- program, 2023-2025 only -- not a substitute).
-- History: the table landed once on 2026-07-27 (~5.19M rows) via
-- scripts/dol_enforce_bulk_load.py, but the chunked write_pandas load
-- corrupted the first column's header (a Snowflake staged-chunk filename got
-- prepended to it instead of a clean ACTIVITY_NR), breaking every downstream
-- query. Someone debugged it that evening, could not fix it in place, and ran
-- DROP TABLE IF EXISTS on it (2026-07-27 19:27) -- it was never reloaded.
-- scripts/fix_errored_models.py already disabled the downstream mart
-- (labor__fed_dol_osha_inspection.sql, enabled=false) for this same reason,
-- but left this staging view enabled and pointed at the dead table -- that is
-- the break the census grid caught (reports/census_grid_2026-08-12/fill/).
-- DO NOT silently "fix" this by relaxing the query -- there is no data to
-- read. A real fix needs someone to re-run scripts/dol_enforce_bulk_load.py
-- (it has a --force flag for exactly this re-pour) AND check the reload for
-- the same column-mangling defect before trusting it -- the root cause of
-- *why* write_pandas produced the bad header was never diagnosed, only that
-- it happened. Left as-is (not disabled) per investigation-session instruction
-- so the break stays visible instead of being paved over.

with source as (
    select * from {{ source('ripple_raw', 'FED_DOL_OSHA_INSPECTION') }}
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
        "_SOURCE_RUN_ID"                             as _source_run_id
    from source
)

select * from renamed
qualify row_number() over (
    partition by activity_nr
    order by _ingested_at desc
) = 1
