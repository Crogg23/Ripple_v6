{{ config(materialized='table', schema='FINANCE') }}

-- Built 2026-08-10 (backlog wave 4). Federal Home Loan Bank members; cert joins to FDIC data, ncua_id to NCUA data, naic_id to NAIC insurer data.
-- Grain: one row = one FHLB member institution (fhfa_id unique). Reads the staging model built alongside it.

select * from {{ ref('stg_fed_fhfa_fhlb_membership__members') }}
