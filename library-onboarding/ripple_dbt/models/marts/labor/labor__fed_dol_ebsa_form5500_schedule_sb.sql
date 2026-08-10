{{ config(materialized='table', schema='LABOR') }}

-- Built 2026-08-10 (backlog wave 4). Form 5500 Schedule SB pension actuarial filings; sb_ein + sb_pn join to other Form 5500 schedules and PBGC plan data.
-- Grain: one row = one Schedule SB filing (ack_id unique). Reads the staging model built alongside it.

select * from {{ ref('stg_fed_dol_ebsa_form5500_schedule_sb__filings') }}
