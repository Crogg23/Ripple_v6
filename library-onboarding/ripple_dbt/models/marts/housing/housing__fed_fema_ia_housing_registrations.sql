{{ config(materialized='table', schema='HOUSING') }}

-- Built 2026-08-10 (backlog wave 3). FEMA Individual Assistance housing registrations
-- (OpenFEMA large-disasters dataset): one row = one valid IA registration
-- (registration_id unique). SAMPLE ONLY -- NOT the full dataset: 3,080,000 of
-- 25,886,797 records (~12%; true count confirmed against OpenFEMA metadata
-- 2026-08-10). Truncated load, not a random sample; full reload queued.
-- Grain: one row = one IA housing registration. Reads the staging model.

select * from {{ ref('stg_fed_fema_ia_housing_registrations__registrations') }}
