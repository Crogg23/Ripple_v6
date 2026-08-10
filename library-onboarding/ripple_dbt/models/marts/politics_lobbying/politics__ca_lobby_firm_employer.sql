{{ config(materialized='table', schema='POLITICS') }}

-- Built 2026-08-09 (73-source backlog, wave 2b). CAL-ACCESS firm-employer billing lines: one row per firm-filing-employer-period (unique with employer name + period start).
-- Grain: one row = one firm-filing-employer-period.

select * from {{ ref('stg_ca_lobby__firm_employer') }}
