{{ config(materialized='table', schema='REFERENCE') }}

-- Built 2026-08-10 (backlog wave 4). ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.
-- Non-publication evidence sources (databases, websites) cited for taxa; one row per source id (with prefix).
-- Grain: one row per source_id_prefix, source_id (1,071 rows), verified live.

select * from {{ ref('stg_fed_itis_other_sources__other_sources') }}
