{{ config(materialized='table', schema='REFERENCE') }}

-- Built 2026-08-10 (backlog wave 4). ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.
-- Bibliographic records for publications cited as taxonomic evidence; one row per publication id (with prefix).
-- Grain: one row per pub_id_prefix, publication_id (30,772 rows), verified live.

select * from {{ ref('stg_fed_itis_publications__publications') }}
