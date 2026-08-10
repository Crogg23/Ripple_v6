{{ config(materialized='table', schema='POLITICS') }}

-- Built 2026-08-09 (73-source backlog, wave 2c). Senate Stock Watcher scrape of senator financial-disclosure trades (name-only source, coverage ends Dec 2020; STOCK Act disclosure-use limits apply -- journalism use only). 546 published exact-duplicate rows kept as landed.
-- Grain: one row = one reported trade line (no unique key).

select * from {{ ref('stg_fed_senate_stock_watcher__transactions') }}
