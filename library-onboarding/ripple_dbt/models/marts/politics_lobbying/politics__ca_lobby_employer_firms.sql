{{ config(materialized='table', schema='POLITICS') }}

-- Built 2026-08-09 (73-source backlog, wave 2b). CAL-ACCESS employer-to-firm engagements: one row per employer-firm-session (unique).
-- Grain: one row = one employer-firm-session.

select * from {{ ref('stg_ca_lobby__employer_firms') }}
