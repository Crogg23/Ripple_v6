{{ config(materialized='table', schema='HOUSING') }}

-- Built 2026-08-10 (backlog wave 4). CFPB HMDA 2017 respondent-ID (ARID) to
-- LEI crosswalk (arid_2017 unique): bridges pre-2018 HMDA lender IDs to the
-- LEIs those lenders reported under in 2018-2020.
-- Grain: one row = one 2017 HMDA respondent. Reads the staging model.

select * from {{ ref('stg_fed_cfpb_hmda_arid2017_lei_xref__xref') }}
