{{ config(materialized='table', schema='POLITICS') }}

-- Built 2026-08-09 (73-source backlog, wave 2b). CAL-ACCESS lobbying registration change log: one row per logged attribute change. filer_id+change_no has 11 published near-duplicates -- no unique test.
-- Grain: one row = one logged change (no unique key as published).

select * from {{ ref('stg_ca_lobby__chg_log') }}
