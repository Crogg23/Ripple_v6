{{ config(materialized='table', schema='FINANCE') }}

-- Built 2026-08-10 (backlog wave 4). Federally insured credit unions with quarterly financials; charter_number joins to NCUA call reports and FHLB membership (ncua_id).
-- Grain: one row = one federally insured credit union (charter_number unique). Reads the staging model built alongside it.

select * from {{ ref('stg_fed_ncua_federally_insured_cu_list__credit_unions') }}
