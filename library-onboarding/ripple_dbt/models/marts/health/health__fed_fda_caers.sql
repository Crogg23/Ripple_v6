{{ config(materialized='table', schema='HEALTH') }}

-- Built 2026-08-09 (73-source backlog, wave 2d). FDA CAERS food/cosmetics adverse-event reports: 85.5k reports flattened from raw openFDA JSON.

select * from {{ ref('stg_fed_fda_caers__all') }}
