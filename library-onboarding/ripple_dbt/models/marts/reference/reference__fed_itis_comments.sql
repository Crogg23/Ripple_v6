{{ config(materialized='table', schema='REFERENCE') }}

-- Built 2026-08-10 (backlog wave 4). ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.
-- Free-text curator comments referenced by the comment-links bridge, keyed by comment id.
-- Grain: one row per comment_id (70,524 rows), verified live.

select * from {{ ref('stg_fed_itis_comments__comments') }}
