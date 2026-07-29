{{ config(materialized='table', schema='HEALTH') }}

-- GRAIN: one row per provider-facility affiliation (NPI + CCN + FACILITY_TYPE)
-- Answers: which providers practise at which facilities -- the NPI <-> CCN bridge
-- Source: CMS Physician Facility Affiliations (2.26M rows)
-- Keys: NPI (provider spine), CCN (facility spine). Both are STEEL-tier join keys,
--       which makes this one of the few tables that links the provider and
--       facility halves of the entity spine.
-- NOTE: this file was a 0-byte stub until 2026-07-29; it parsed but would have
--       failed `dbt build`.

select
    NPI,
    IND_PAC_ID,
    PROVIDER_LAST_NAME,
    PROVIDER_FIRST_NAME,
    PROVIDER_MIDDLE_NAME,
    SUFF                                as NAME_SUFFIX,
    FACILITY_TYPE,
    CCN,
    FACILITY_TYPE_CERTIFICATION_NUMBER
from {{ source('ripple_raw', 'FED_CMS_FACILITY_AFFILIATION') }}
where NPI is not null
