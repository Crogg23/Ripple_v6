{{ config(materialized='table', schema='HOUSING') }}

-- Built 2026-08-10 (backlog wave 4). HUD FHA Multifamily Firm Commitment
-- Activity (FY2001 - Q3 FY2026): one row per firm commitment activity with
-- project, lender, mortgage amount, units, and subsidy flags (LIHTC, bonds,
-- HOME, CDBG, etc.). Excel preamble/header/count rows are dropped in staging
-- by keeping only numeric FHA Numbers; surrogate commitment_record_id
-- (fha_number + firm_activity_date + tiebreaker).
-- Grain: one row = one firm commitment activity. Reads the staging model.

select * from {{ ref('stg_fed_hud_mf_firm_commitments__commitments') }}
