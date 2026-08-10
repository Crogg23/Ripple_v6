{{ config(materialized='table', schema='POLITICS') }}

-- Built 2026-08-09 (73-source backlog, wave 2b). CAL-ACCESS in-house lobbyist roster: one row per lobbyist-employer-session (unique).
-- Grain: one row = one lobbyist-employer-session.

select * from {{ ref('stg_ca_lobby__emp_lobbyist') }}
