{{ config(materialized='table', schema='POLITICS') }}

-- Built 2026-08-09 (73-source backlog, wave 2b). Texas lobby award/memento expenditures: one row per activity (lobbyactivityid unique).
-- Grain: one row = one award activity.

select * from {{ ref('stg_tx_lobby__awards') }}
