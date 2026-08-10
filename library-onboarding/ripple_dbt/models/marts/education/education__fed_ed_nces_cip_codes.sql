{{ config(materialized='table', schema='EDUCATION') }}

-- Built 2026-08-10 (backlog wave 4). NCES CIP-2020 Classification of
-- Instructional Programs: program codes, titles, and definitions at all
-- hierarchy levels (Excel ="..." armor stripped in staging).
-- Grain: one row = one CIP code (cip_code unique, 2,318 rows).

select * from {{ ref('stg_fed_ed_nces_cip_codes__cip_codes') }}
