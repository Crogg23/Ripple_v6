{{ config(materialized='table', schema='TRANSPORT') }}

-- Built 2026-08-09 (73-source backlog). FRA Form 57 highway-rail grade
-- crossing incidents. Grain: one row = one incident report; 24 duplicate
-- report keys (amended/joint filings) kept as landed — no unique test.

select * from {{ ref('stg_fed_fra_crossing_incidents__all') }}
