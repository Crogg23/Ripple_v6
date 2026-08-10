{{ config(materialized='table', schema='REFERENCE') }}

-- Built 2026-08-10 (backlog wave 4). Crossref Funder Registry: funder DOI URIs
-- with display names and replacement pointers for deprecated ids.
-- Grain: one row = one funder URI (unique, 45,661 rows). funder_uri is the
-- FundRef crosswalk join key (e.g. to ROR external ids).

select * from {{ ref('stg_xc_crossref_funder_registry__funders') }}
