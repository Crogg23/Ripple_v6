{{ config(materialized='table', schema='REFERENCE') }}

-- Built 2026-08-10 (backlog wave 4). ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.
-- Core taxonomic units table: one row per taxonomic serial number (TSN) with name parts, usage/validity, credibility ratings, parent TSN, author, kingdom and rank.
-- Grain: one row per tsn (993,346 rows), verified live.

select * from {{ ref('stg_fed_itis_taxonomic_units__taxa') }}
