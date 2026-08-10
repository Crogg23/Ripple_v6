{{ config(materialized='table', schema='POLITICS') }}

-- Built 2026-08-09 (73-source backlog, wave 2b). Texas lobby food & beverage expenditures on state officials: one row per activity (lobbyactivityid unique).
-- Grain: one row = one food/beverage activity.

select * from {{ ref('stg_tx_lobby__food_beverage') }}
