{{ config(materialized='table', schema='REFERENCE') }}

-- Built 2026-08-10 (backlog wave 4). ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.
-- Materialized taxonomic tree: one row per TSN with its full hierarchy string, parent TSN, tree level and child count (valid/accepted taxa only).
-- Grain: one row per tsn (678,363 rows), verified live.

select * from {{ ref('stg_fed_itis_hierarchy__hierarchy') }}
