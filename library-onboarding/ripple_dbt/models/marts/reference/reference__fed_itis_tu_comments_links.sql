{{ config(materialized='table', schema='REFERENCE') }}

-- Built 2026-08-10 (backlog wave 4). ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.
-- Bridge linking taxa to free-text curator comments; one row per TSN x comment id.
-- Grain: one row per tsn, comment_id (192,851 rows), verified live.

select * from {{ ref('stg_fed_itis_tu_comments_links__comment_links') }}
