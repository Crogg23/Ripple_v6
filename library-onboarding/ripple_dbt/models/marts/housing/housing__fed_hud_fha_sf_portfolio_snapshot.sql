{{ config(materialized='table', schema='HOUSING') }}

-- Built 2026-08-10 (backlog wave 4). HUD FHA Single-Family Portfolio Snapshot:
-- loan-level FHA endorsements with lender, property location, rate, and amount.
-- No natural key in the source file; surrogate loan_record_id (state + zip +
-- originating mortgagee number + endorsement year/month + row_number over
-- full-row hash) is documented in staging.
-- Grain: one row = one endorsed FHA single-family loan. Reads the staging model.

select * from {{ ref('stg_fed_hud_fha_sf_portfolio_snapshot__loans') }}
