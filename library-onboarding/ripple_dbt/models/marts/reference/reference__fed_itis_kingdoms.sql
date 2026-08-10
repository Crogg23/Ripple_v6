{{ config(materialized='table', schema='REFERENCE') }}

-- Built 2026-08-10 (backlog wave 4). ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.
-- The seven ITIS kingdoms of life, keyed by kingdom id.
-- Grain: one row per kingdom_id (7 rows), verified live.

select * from {{ ref('stg_fed_itis_kingdoms__kingdoms') }}
