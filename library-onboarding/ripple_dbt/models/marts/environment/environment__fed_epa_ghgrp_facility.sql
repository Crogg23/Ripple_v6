{{ config(materialized='table', schema='ENVIRONMENT') }}

-- Built 2026-08-10 (backlog wave 4). EPA GHGRP facility registry: name, address, lat/long, NAICS, parent company, and FRS_ID (cross-dataset join key to EPA FRS/ECHO/ICIS).
-- Grain: one row = one facility x reporting year (facility_id + year exactly unique).

select * from {{ ref('stg_fed_epa_ghgrp_facility__facilities') }}
