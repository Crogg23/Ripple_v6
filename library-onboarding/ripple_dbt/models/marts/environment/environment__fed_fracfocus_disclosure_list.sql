{{ config(materialized='table', schema='ENVIRONMENT') }}

-- Built 2026-08-10 (73-source backlog, wave 3). FracFocus disclosure list —
-- the well/job header extract of the fracking chemical registry (248,835
-- rows). Grain: one row = one well fracturing job disclosure (disclosure_id
-- unique). Operator, API well number, location, dates, and base fluid volumes.

select * from {{ ref('stg_fed_fracfocus_disclosure_list__disclosures') }}
