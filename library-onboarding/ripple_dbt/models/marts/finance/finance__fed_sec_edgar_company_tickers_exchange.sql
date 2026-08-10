{{ config(materialized='table', schema='FINANCE') }}

-- Rebuilt 2026-08-10 (wave 4) against the re-ingested landing table (10,398
-- rows, exact-unique on CIK + TICKER); replaces the stale generated 1-row
-- FIELDS/DATA passthrough. SEC EDGAR company_tickers_exchange: CIK ↔ ticker ↔
-- exchange reference. CIK is the join key to all SEC data on the platform.
-- Grain: one row = one (CIK, ticker) listing; cik_ticker is the tested key.

select * from {{ ref('stg_fed_sec_edgar_company_tickers_exchange__tickers') }}
