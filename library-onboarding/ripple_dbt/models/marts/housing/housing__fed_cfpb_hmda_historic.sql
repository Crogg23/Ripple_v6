{{ config(materialized='table', schema='HOUSING') }}

-- Built 2026-08-10 (backlog wave 3). CFPB HMDA Historic: pre-2018 LAR loan-application
-- records (surrogate lar_record_id; no natural key). Coverage is AS_OF_YEAR 2015-2017
-- ONLY -- "historic" means the pre-2018 LAR file format, and only 2015-2017 are landed.
-- Lender join key is respondent_id (legacy Respondent ID), NOT lei.
-- Grain: one row = one anonymized loan-application record. Reads the staging model.

select * from {{ ref('stg_fed_cfpb_hmda_historic__lar_records') }}
