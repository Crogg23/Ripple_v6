{{ config(materialized='table', schema='POLITICS') }}

-- Built 2026-08-09 (73-source backlog, wave 2b). Texas lobby on-behalf-of lines: one row per client an expenditure was made on behalf of (lobbyexpendonbehalfid unique).
-- Grain: one row = one on-behalf-of line.

select * from {{ ref('stg_tx_lobby__individual_reporting') }}
