{{ config(materialized='table', schema='FINANCE') }}

-- Built 2026-08-11. NCUA call report FS220 file: core financial statement per credit union for the
-- 2026-03 cycle (~245 ACCT_* measures; acct_010 = total assets). cu_number joins to
-- finance__fed_ncua_call_reports_foicu (roster/profile). Replaces the retired finance__fed_ncua_call_reports.
-- Grain: one row = one credit union's financial statement (cu_number unique). Reads the staging model built alongside it.

select * from {{ ref('stg_fed_ncua_call_reports__fs220') }}
