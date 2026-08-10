{{ config(materialized='table', schema='HEALTH') }}

-- Built 2026-08-10 (backlog wave 4). Indian Health Service Standard Code Book
-- facilities: ASUFAC-coded facility list with area, service unit, type, bed
-- count, and IHS/Tribal/Urban operator code.
-- Grain: scb_facility_id (surrogate over near-unique asufac_code,
-- 8,731 distinct of 8,733 rows).

select * from {{ ref('stg_fed_ihs_scb_facility__facilities') }}
