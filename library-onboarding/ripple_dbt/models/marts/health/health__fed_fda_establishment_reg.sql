{{ config(materialized='table', schema='HEALTH') }}

-- Built 2026-08-09 (73-source backlog, wave 2d). FDA device establishment registrations: 330k registration-product rows flattened from raw openFDA JSON.

select * from {{ ref('stg_fed_fda_establishment_reg__all') }}
