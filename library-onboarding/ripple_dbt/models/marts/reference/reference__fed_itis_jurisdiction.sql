{{ config(materialized='table', schema='REFERENCE') }}

-- Built 2026-08-10 (backlog wave 4). ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.
-- Jurisdictional occurrence of each taxon (e.g. Continental US, Alaska, Canada) with native/introduced origin; one row per TSN x jurisdiction.
-- Grain: one row per tsn, jurisdiction_value (161,922 rows), verified live.

select * from {{ ref('stg_fed_itis_jurisdiction__jurisdictions') }}
