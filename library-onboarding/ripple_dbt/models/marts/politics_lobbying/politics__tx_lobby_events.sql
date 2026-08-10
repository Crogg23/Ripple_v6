{{ config(materialized='table', schema='POLITICS') }}

-- Built 2026-08-09 (73-source backlog, wave 2b). Texas lobby event expenditures (ceremonies/receptions for officials): one row per activity (lobbyactivityid unique).
-- Grain: one row = one event activity.

select * from {{ ref('stg_tx_lobby__events') }}
