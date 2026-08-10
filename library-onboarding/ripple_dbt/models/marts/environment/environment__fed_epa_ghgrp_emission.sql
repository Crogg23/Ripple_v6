{{ config(materialized='table', schema='ENVIRONMENT') }}

-- Built 2026-08-10 (backlog wave 4). EPA Greenhouse Gas Reporting Program: facility-level CO2e emissions by gas, sector, and subsector, 2010+.
-- Grain: one row = one facility x year x sector x subsector x gas emission record (surrogate-keyed; 81 composite collisions tiebroken deterministically).

select * from {{ ref('stg_fed_epa_ghgrp_emission__emissions') }}
