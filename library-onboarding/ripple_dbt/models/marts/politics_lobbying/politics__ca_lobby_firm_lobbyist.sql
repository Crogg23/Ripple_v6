{{ config(materialized='table', schema='POLITICS') }}

-- Built 2026-08-09 (73-source backlog, wave 2b). CAL-ACCESS firm lobbyist roster: one row per lobbyist-firm-session (unique).
-- Grain: one row = one lobbyist-firm-session.

select * from {{ ref('stg_ca_lobby__firm_lobbyist') }}
