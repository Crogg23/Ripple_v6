{{ config(materialized='table', schema='POLITICS') }}

-- Built 2026-08-09 (73-source backlog, wave 2b). IRS Form 8872 periodic reports of 527 orgs (contribution/expenditure totals; form_id_number unique).
-- Grain: one row = one Form 8872 report.

select * from {{ ref('stg_irs527__8872_reports') }}
