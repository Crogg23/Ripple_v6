{{ config(materialized='table', schema='HEALTH') }}

-- Built 2026-08-09 (73-source backlog, wave 2c). HRSA UDS Table 3A: federally-funded health center patient counts by age/sex line (bhcmisid unique). Column pairs are (male, female) per age line.
-- Grain: one row = one health center's Table 3A.

select * from {{ ref('stg_fed_hrsa_uds_table3a_patients__by_center') }}
