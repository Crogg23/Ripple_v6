{{ config(materialized='table', schema='JUSTICE') }}

-- Built 2026-08-09 (73-source backlog, wave 2c). Judicial Panel on Multidistrict Litigation: pending MDLs (mdl_no unique) with district, judge, and pending/total action counts.
-- Grain: one row = one pending MDL. Reads the pre-existing staging model.

select * from {{ ref('stg_fed_jpml_pending_mdls__mdl_docket') }}
