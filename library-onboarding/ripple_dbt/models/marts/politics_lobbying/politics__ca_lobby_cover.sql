{{ config(materialized='table', schema='POLITICS') }}

-- Built 2026-08-09 (73-source backlog, wave 2b). CAL-ACCESS lobbying disclosure cover pages (Forms 615/625/635/645...): one row per filing version (filing_id + amend_id unique).
-- Grain: one row = one filing version (filing_id + amend_id). Reads the pre-existing staging model.

select * from {{ ref('stg_ca_lobby_cover__filings') }}
