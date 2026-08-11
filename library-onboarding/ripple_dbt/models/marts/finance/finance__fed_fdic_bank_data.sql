{{ config(materialized='table', schema='FINANCE') }}

-- Built 2026-08-09 (73-source backlog, wave 2d). FULL DATASET as of 2026-08-11:
-- all 27,836 FDIC-insured institutions, active and historical -- exactly the total
-- the API advertises, with CERT unique across every row. Replaced a 10,000-row
-- slice that had carried a sample-only label. Loader: scripts/fdic_institutions_load.py.
-- Now also carries LEI, the global entity identifier -- but FDIC publishes it
-- TRUNCATED to 16 characters against a real LEI's 20, so an equality join to
-- GLEIF matches nothing. Join on LEFT(gleif.LEI,16) instead: that matches 2,224
-- of the 2,252 banks carrying one. Only ~8% of institutions have an LEI at all.
-- See the staging model's header for the full check.
-- Grain: one row = one insured institution (CERT unique).

select * from {{ ref('stg_fed_fdic_bank_data__institutions') }}
