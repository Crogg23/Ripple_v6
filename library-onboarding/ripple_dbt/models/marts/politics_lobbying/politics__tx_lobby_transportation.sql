{{ config(materialized='table', schema='POLITICS') }}

-- Built 2026-08-09 (73-source backlog, wave 2b). Texas lobby transportation/lodging expenditures: one row per travel line (lobactivitytravelid unique; lobbyactivityid repeats across legs).
-- Grain: one row = one travel line.

select * from {{ ref('stg_tx_lobby__transportation') }}
