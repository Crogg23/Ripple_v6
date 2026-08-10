{{ config(materialized='table', schema='JUSTICE') }}

-- Built 2026-08-10 (backlog wave 3). Federal Judicial Center Integrated Database: courts of appeals case files (988K records).
-- Grain: one row = one appeal record per snapshot; (circuit, docket, reopen, tapeyear, dktdate) is exactly unique, no tiebreaker needed.

select * from {{ ref('stg_fed_fjc_idb_appellate__appeal_records') }}
