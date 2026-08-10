{{ config(materialized='table', schema='FINANCE') }}

-- Built 2026-08-10 (backlog wave 4). PCAOB Form AP filings: which audit partner signed which public-company audit; issuer_cik joins to SEC EDGAR/DERA data.
-- Grain: one row = one Form AP filing (FORM_FILING_ID exactly unique).

select * from {{ ref('stg_fed_pcaob_form_ap_filings__filings') }}
