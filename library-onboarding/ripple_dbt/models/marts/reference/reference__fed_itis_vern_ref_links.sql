{{ config(materialized='table', schema='REFERENCE') }}

-- Built 2026-08-10 (backlog wave 4). ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.
-- Links vernacular names to their supporting documents; one row per TSN x document x vernacular id.
-- Grain: one row per tsn, doc_id_prefix, documentation_id, vern_id (93,078 rows), verified live.

select * from {{ ref('stg_fed_itis_vern_ref_links__vernacular_ref_links') }}
