{{ config(materialized='table', schema='HOUSING') }}

-- Built 2026-08-10 (backlog wave 4). SAMPLE ONLY -- NOT the full dataset:
-- 17,474 HMDA LAR loan-application records out of a multi-million-row
-- national corpus. Use for shape/testing, never for lending-pattern claims.
-- Loan-level; LEI + activity_year is NOT unique, so surrogate lar_record_id
-- (lei + activity_year + row_number over full-row hash) is documented in
-- staging. All 102 source columns kept with sensible casts.
-- Grain: one row = one anonymized loan-application record. Reads the staging model.

select * from {{ ref('stg_fed_cfpb_hmda_lar__lar_records') }}
