{{ config(materialized='table', schema='HEALTH') }}

-- Built 2026-08-10 (backlog wave 4). HRSA primary-care Health Professional
-- Shortage Area designations: one row per HPSA x geography component, with
-- scores, shortage measures, and full geography rollups.
-- Grain: hpsa_component_id (surrogate over near-unique hpsa_id + geography id).

select * from {{ ref('stg_fed_hrsa_hpsa_primary_care__designations') }}
