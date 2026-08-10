{{ config(materialized='table', schema='FINANCE') }}

-- Built 2026-08-09 (73-source backlog, wave 2). IRS FATCA FFI list.
-- Grain: one row = one registered foreign financial institution (GIIN unique).
-- Key joins: GIIN; institution name + country for fuzzy crosswalks.

select * from {{ ref('stg_fed_fatca_ffi__institutions') }}
