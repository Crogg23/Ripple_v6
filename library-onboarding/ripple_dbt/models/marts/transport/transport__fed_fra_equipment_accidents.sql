{{ config(materialized='table', schema='TRANSPORT') }}

-- Built 2026-08-09 (73-source backlog). FRA Form 54 rail equipment
-- accidents. Grain: one row = one railroad's report of an accident — the
-- same accident appears once per involved railroad plus amended filings
-- (report_key NOT unique; 197,234 distinct / 224,941 rows). Kept as landed;
-- aggregate with care (see transport__fed_fra_rail_deaths_by_railroad for
-- the double-count-safe deaths rollup, built from casualties instead).

select * from {{ ref('stg_fed_fra_equipment_accidents__all') }}
