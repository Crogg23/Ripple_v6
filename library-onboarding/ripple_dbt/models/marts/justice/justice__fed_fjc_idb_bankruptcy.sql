{{ config(materialized='table', schema='JUSTICE') }}

-- Built 2026-08-10 (backlog wave 3). Federal Judicial Center Integrated Database: bankruptcy case files (7.0M records).
-- Grain: one row = one bankruptcy case per snapshot; (case_key, snapshot) is exactly unique, no tiebreaker needed.

select * from {{ ref('stg_fed_fjc_idb_bankruptcy__case_snapshots') }}
