{{ config(materialized='table', schema='JUSTICE') }}

-- Built 2026-08-09 (73-source backlog). OpenSanctions default collection:
-- every person, company, vessel, aircraft and crypto wallet currently
-- targeted by a sanctions/PEP/enforcement dataset worldwide, consolidated
-- and deduplicated by OpenSanctions. Distinct from justice__intl_opensanctions
-- (the smaller sanctions-only consolidated list).
-- Grain: one row = one target (id unique).

select * from {{ ref('stg_intl_opensanctions_default__targets') }}
