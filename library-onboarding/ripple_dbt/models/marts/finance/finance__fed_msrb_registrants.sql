{{ config(materialized='table', schema='FINANCE') }}

-- Built 2026-08-10 (backlog wave 4). Municipal Securities Rulemaking Board registrants (dealers and municipal advisors).
-- Grain: one row = one registrant per registrant type (MSRB_ID + REGISTRANT_TYPE exactly unique). Reads the staging model built alongside it.

select * from {{ ref('stg_fed_msrb_registrants__registrants') }}
