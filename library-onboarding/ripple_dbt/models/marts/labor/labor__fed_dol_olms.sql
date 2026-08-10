{{ config(materialized='table', schema='LABOR') }}

-- Built 2026-08-10 (backlog wave 4). DOL OLMS union financial disclosure filings (LM-2/LM-3/LM-4, 2000-2026): one row per LM filing with headline totals — assets, liabilities, receipts, disbursements, members. file_number (OLMS file number) is the union entity key linking a union's filings across years; rpt_id is near-unique, so filing_record_id carries a deterministic tiebreaker.
-- Grain: one row = one LM filing. Reads the staging model.

select * from {{ ref('stg_fed_dol_olms__filings') }}
