{{ config(materialized='table', schema='REFERENCE') }}

-- Built 2026-08-10 (backlog wave 4). ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.
-- Lookup of the assembled complete scientific name for every TSN.
-- Grain: one row per tsn (993,346 rows), verified live.

select * from {{ ref('stg_fed_itis_longnames__complete_names') }}
