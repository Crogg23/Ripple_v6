{{ config(materialized='table', schema='HOUSING') }}

-- Built 2026-08-10 (backlog wave 4). HUD multifamily Section 8 (and related
-- programs) rental-assistance contracts from TRACS: effective/expiration
-- dates, status, assisted unit counts by bedroom size, and rent-to-FMR ratio.
-- CONTRACT_NUMBER is near-unique (24,308/24,309); surrogate
-- contract_record_id adds a full-row-hash tiebreaker.
-- Grain: one row = one Section 8 contract record. Reads the staging model.

select * from {{ ref('stg_fed_hud_mf_section8_contracts__contracts') }}
