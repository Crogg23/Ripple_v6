{{ config(materialized='table', schema='ENVIRONMENT') }}

-- Built 2026-08-10 (backlog wave 4). EPA TRI facility registry; frs_id and epa_registry_id join to EPA FRS, tri_facility_id joins to TRI release data.
-- Grain: one row = one TRI facility (tri_facility_id unique). Reads the staging model built alongside it.

select * from {{ ref('stg_fed_epa_tri_facility__facilities') }}
