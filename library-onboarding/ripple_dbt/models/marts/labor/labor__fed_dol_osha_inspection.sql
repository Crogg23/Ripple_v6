{{ config(materialized='table', schema='LABOR') }}

-- GRAIN: one row per inspection (activity_nr is unique)
-- Answers: Which employers have been inspected by OSHA, how often, and for what?
-- Source: DOL OSHA Inspections (~5.2M records, 1970s–present)
-- Key joins: naics_code → industry; site_state + site_zip → geography; estab_name → entity resolution

select
    activity_nr,
    reporting_id,
    estab_name,
    site_address,
    site_city,
    site_state,
    site_zip,
    owner_type,
    owner_code,
    sic_code,
    naics_code,
    insp_type,
    insp_scope,
    safety_hlth,
    union_status,
    adv_notice,
    nr_in_estab,
    open_date,
    case_mod_date,
    close_conf_date,
    close_case_date,
    (close_case_date is not null) as is_closed,
    _ingested_at,
    _source_run_id
from {{ ref('stg_fed_dol_osha_inspection__all') }}
