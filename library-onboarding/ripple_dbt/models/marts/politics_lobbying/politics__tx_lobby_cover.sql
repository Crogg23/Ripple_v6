{{ config(materialized='table', schema='POLITICS') }}

-- Built 2026-08-09 (73-source backlog, wave 2b). Texas Ethics Commission lobby activity report cover sheets (Form LA): one row per report (reportinfoident unique) with per-category expenditure totals.
-- Grain: one row = one lobby activity report. Reads the pre-existing staging model.

select * from {{ ref('stg_tx_lobby_cover__reports') }}
