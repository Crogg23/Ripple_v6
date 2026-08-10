{{ config(materialized='table', schema='HOUSING') }}

-- Built 2026-08-09 (73-source backlog, wave 2d). SAMPLE ONLY -- NOT the full dataset. HMDA mortgage loan-level records: a single state-year slice (Washington DC, 2023; 28,301 rows) of a corpus that is ~50 states x 2018-present. Use for shape/testing, never for lending-pattern claims. Full pull needs a state x year loop loader.
-- Grain: one row = one reported loan/application (no unique key in the export).

select * from {{ ref('stg_fed_cfpb_hmda__loans') }}
