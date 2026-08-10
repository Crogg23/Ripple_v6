{{ config(materialized='table', schema='REFERENCE') }}

-- Built 2026-08-10 (backlog wave 4). ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.
-- Common (vernacular) names for taxa in multiple languages; one row per TSN x vernacular id.
-- Grain: one row per tsn, vern_id (166,778 rows), verified live.

select * from {{ ref('stg_fed_itis_vernaculars__vernacular_names') }}
