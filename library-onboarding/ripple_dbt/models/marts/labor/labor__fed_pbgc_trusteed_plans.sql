{{ config(materialized='table', schema='LABOR') }}

-- Built 2026-08-09 (73-source backlog, wave 2c). PBGC trusteed single-employer pension plans (failed plans taken over by the federal insurer): one row per case (case_number unique) with sponsor, EIN, termination/trusteeship dates, participant count.
-- Grain: one row = one trusteed plan case.

select * from {{ ref('stg_fed_pbgc_trusteed_plans__plans') }}
