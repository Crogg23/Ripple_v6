{{ config(materialized='table', schema='POLITICS') }}

-- Built 2026-08-09 (73-source backlog, wave 2b). IRS Form 8871 election authority identification numbers: one row per EAIN per form (form_id + eain_id unique).
-- Grain: one row = one EAIN listing.

select * from {{ ref('stg_irs527__eain') }}
