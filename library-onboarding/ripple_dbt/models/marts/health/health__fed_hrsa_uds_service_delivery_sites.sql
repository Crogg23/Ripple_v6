{{ config(materialized='table', schema='HEALTH') }}

-- Built 2026-08-10 (backlog wave 4). HRSA UDS federally-funded health-center
-- service delivery sites (FQHCs and look-alikes) with site NPI / Medicare
-- billing number, parent health center, and congressional geography.
-- Grain: one row = one site (bphc_assigned_number, verified unique).

select * from {{ ref('stg_fed_hrsa_uds_service_delivery_sites__sites') }}
