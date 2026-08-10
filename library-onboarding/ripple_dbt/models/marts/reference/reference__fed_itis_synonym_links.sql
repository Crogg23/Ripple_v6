{{ config(materialized='table', schema='REFERENCE') }}

-- Built 2026-08-10 (backlog wave 4). ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.
-- Synonym mapping from a non-accepted TSN to its accepted TSN; one row per synonym pair.
-- Grain: one row per tsn, tsn_accepted (315,254 rows), verified live.

select * from {{ ref('stg_fed_itis_synonym_links__synonyms') }}
