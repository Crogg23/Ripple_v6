{{ config(materialized='table', schema='POLITICS') }}

-- Built 2026-08-09 (73-source backlog, wave 2b). CAL-ACCESS lobbyist employer session totals: one row per employer per legislative session (4 published doubles in the 1999 session -- no unique test).
-- Grain: one row = one employer-session.

select * from {{ ref('stg_ca_lobby__employer') }}
