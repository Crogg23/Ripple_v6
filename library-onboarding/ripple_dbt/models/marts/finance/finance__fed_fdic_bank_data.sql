{{ config(materialized='table', schema='FINANCE') }}

-- Built 2026-08-09 (73-source backlog, wave 2d). SAMPLE ONLY -- NOT the full dataset. FDIC insured-institution directory: a 10,000-row API slice (cert number unique within it) of the full multi-decade institution universe. Use for shape/testing only; full pull needs an offset-paginated loader.
-- Grain: one row = one insured institution (cert unique in the slice).

select * from {{ ref('stg_fed_fdic_bank_data__institutions') }}
