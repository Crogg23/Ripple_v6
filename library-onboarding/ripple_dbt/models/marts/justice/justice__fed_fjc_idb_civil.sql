{{ config(materialized='table', schema='JUSTICE') }}

-- Built 2026-08-10 (backlog wave 3). Federal Judicial Center Integrated Database: civil case files (10.9M records).
-- Grain: one row = one civil case record per snapshot year (case_record_id unique; near-unique composite plus provenance tiebreaker).
-- TAPEYEAR '2099' (462,223 rows) is FJC's convention for the pending-cases file, kept as published.

select * from {{ ref('stg_fed_fjc_idb_civil__case_records') }}
