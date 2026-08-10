{{ config(materialized='table', schema='REFERENCE') }}

-- Built 2026-08-10 (backlog wave 4). ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.
-- Companion lookup with a stripped/normalized short form of each taxon author string, keyed by author id.
-- Grain: one row per taxon_author_id (214,445 rows), verified live.

select * from {{ ref('stg_fed_itis_strippedauthor__stripped_authors') }}
