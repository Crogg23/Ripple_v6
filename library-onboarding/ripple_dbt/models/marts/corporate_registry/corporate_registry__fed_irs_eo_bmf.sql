{{ config(materialized='table', schema='CORPORATE_REGISTRY') }}

-- Built 2026-08-09 (73-source backlog, wave 2). IRS Exempt Organizations
-- Business Master File, full national extract.
-- Grain: one row = one tax-exempt organization (EIN unique).
-- Key joins: EIN -> IRS 527 orgs, Form 5500 sponsors, FATCA FFI list.

select * from {{ ref('stg_fed_irs_eo_bmf__orgs') }}
