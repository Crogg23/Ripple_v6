{{ config(materialized='table', schema='REFERENCE') }}

-- Built 2026-08-10 (backlog wave 4). ROR (Research Organization Registry): global
-- registry of research organizations with GRID / ISNI / Wikidata / FundRef /
-- GeoNames crosswalk identifiers as join keys.
-- Grain: one row = one ROR organization (ror_id unique, 135,710 rows).

select * from {{ ref('stg_xc_ror_research_organizations__organizations') }}
