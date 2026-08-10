{{ config(materialized='table', schema='JUSTICE') }}

-- Built 2026-08-10 (backlog wave 3). Federal Judicial Center Integrated Database: criminal defendant files (6.3M records).
-- Grain: one row = one defendant-case record per snapshot (defendant_record_id unique; near-unique composite plus provenance tiebreaker).
-- The 5x repeated filing-offense and termination-offense/sentence column groups stay as published, renamed snake_case.

select * from {{ ref('stg_fed_fjc_idb_criminal__defendant_records') }}
