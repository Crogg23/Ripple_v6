{{ config(materialized='table', schema='ENVIRONMENT') }}

-- Built 2026-08-09 (73-source backlog, wave 2d). SAMPLE ONLY -- NOT the full dataset. EPA Envirofacts API: a 5,000-row slice of ONE program table (TRI facility names); FRS/site/handler id columns are blank in this slice. Use for shape/testing only.
-- Grain: one row = one facility-name row from the TRI slice (no key).

select * from {{ ref('stg_fed_epa_envirofacts__facility_sample') }}
