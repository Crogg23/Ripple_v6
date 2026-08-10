{{ config(materialized='table', schema='REFERENCE') }}

-- Built 2026-08-10 (backlog wave 4). ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.
-- Lookup of taxon author citations (the naming authority string attached to scientific names), keyed by author id.
-- Grain: one row per taxon_author_id (214,445 rows), verified live.

select * from {{ ref('stg_fed_itis_taxon_authors_lkp__authors') }}
