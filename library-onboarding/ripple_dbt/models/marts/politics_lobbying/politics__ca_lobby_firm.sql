{{ config(materialized='table', schema='POLITICS') }}

-- Built 2026-08-09 (73-source backlog, wave 2b). CAL-ACCESS lobbying firm session totals: one row per firm per session (firm_id + session_id unique).
-- Grain: one row = one firm-session.

select * from {{ ref('stg_ca_lobby__firm') }}
