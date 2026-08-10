{{ config(materialized='table', schema='POLITICS') }}

-- Built 2026-08-09 (73-source backlog, wave 2b). Texas lobby subject-matter lines: one row per reported subject matter (lobbysubjectmatterid unique).
-- Grain: one row = one subject-matter line.

select * from {{ ref('stg_tx_lobby__subject_matter') }}
