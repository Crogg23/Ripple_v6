{{ config(materialized='table', schema='HEALTH') }}

-- Built 2026-08-09 (73-source backlog, wave 2c). HRSA UDS health center directory: one row per federally-funded health center (bhcmisid unique) with address, director, funding streams, urban/rural flag.
-- Grain: one row = one health center.

select * from {{ ref('stg_fed_hrsa_uds_health_center_info__centers') }}
