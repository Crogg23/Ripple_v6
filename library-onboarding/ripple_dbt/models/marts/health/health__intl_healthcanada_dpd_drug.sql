{{ config(materialized='table', schema='HEALTH') }}

-- Built 2026-08-10 (backlog wave 4). Health Canada Drug Product Database
-- (DPD) drug products with DIN, brand name, class, and AI group.
-- Grain: one row = one drug_code (verified unique).
-- One record is missing: the loader consumed the first data row as the
-- column header (columns renamed positionally in staging).

select * from {{ ref('stg_intl_healthcanada_dpd_drug__drugs') }}
