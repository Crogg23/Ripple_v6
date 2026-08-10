{{ config(materialized='table', schema='REFERENCE') }}

-- Built 2026-08-10 (backlog wave 4). ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.
-- Crosswalk from legacy NOAA/NODC taxonomic codes to ITIS TSNs; one row per NODC id x TSN.
-- Grain: one row per nodc_id, tsn (209,565 rows), verified live.

select * from {{ ref('stg_fed_itis_nodc_ids__nodc_ids') }}
