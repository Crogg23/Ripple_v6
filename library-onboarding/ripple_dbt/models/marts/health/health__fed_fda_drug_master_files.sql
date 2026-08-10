{{ config(materialized='table', schema='HEALTH') }}

-- Built 2026-08-10 (backlog wave 4). FDA Drug Master File registry: one row
-- per DMF number with holder company, subject, type, status, and submit date.
-- Grain: one row = one DMF (dmf_number, verified unique).

select * from {{ ref('stg_fed_fda_drug_master_files__dmfs') }}
