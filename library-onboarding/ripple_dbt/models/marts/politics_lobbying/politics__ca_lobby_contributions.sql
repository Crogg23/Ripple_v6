{{ config(materialized='table', schema='POLITICS') }}

-- Built 2026-08-09 (73-source backlog, wave 2b). CAL-ACCESS lobbyist campaign contributions: one row per reported contribution. CONTRIBUTION_DT blank on many rows as published.
-- Grain: one row = one reported contribution (no unique key).

select * from {{ ref('stg_ca_lobby__contributions') }}
