{{ config(materialized='table', schema='FINANCE') }}

-- Built 2026-08-10 (backlog wave 4). SEC investment-company series/class registry; cik_number joins to EDGAR/DERA, class_ticker joins to market data.
-- Grain: one row = one fund share class record (series_class_record_id). Reads the staging model built alongside it.

select * from {{ ref('stg_fed_sec_investment_company_series_class__series_classes') }}
