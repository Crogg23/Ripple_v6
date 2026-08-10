{{ config(materialized='table', schema='REFERENCE') }}

-- Built 2026-08-10 (backlog wave 4). ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.
-- Links taxa to the publications/experts/other-source documents that support them; one row per TSN x document.
-- Grain: one row per tsn, doc_id_prefix, documentation_id (1,970,107 rows), verified live.

select * from {{ ref('stg_fed_itis_reference_links__reference_links') }}
