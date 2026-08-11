{{ config(materialized='table', schema='FINANCE') }}

-- Built 2026-08-11. NCUA call report FOICU file: federally insured credit union roster/profile for the
-- 2026-03 cycle. cu_number joins to finance__fed_ncua_call_reports_fs220 (financials); RSSD links to
-- Fed/FFIEC identifiers. Replaces the retired finance__fed_ncua_call_reports (built on a data dictionary).
-- Grain: one row = one federally insured credit union (cu_number unique). Reads the staging model built alongside it.

select * from {{ ref('stg_fed_ncua_call_reports__foicu') }}
