{{ config(materialized='table', schema='REFERENCE') }}

-- Built 2026-08-10 (backlog wave 4). ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.
-- Geographic divisions (continental/oceanic regions) in which each taxon occurs; one row per TSN x geographic value.
-- Grain: one row per tsn, geographic_value (480,351 rows), verified live.

select * from {{ ref('stg_fed_itis_geographic_div__geographic_divisions') }}
