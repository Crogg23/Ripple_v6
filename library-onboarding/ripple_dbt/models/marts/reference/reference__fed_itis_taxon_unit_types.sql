{{ config(materialized='table', schema='REFERENCE') }}

-- Built 2026-08-10 (backlog wave 4). ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.
-- Rank definitions per kingdom (Kingdom/Phylum/.../Species etc.) with required-parent rank rules; one row per kingdom x rank.
-- Grain: one row per kingdom_id, rank_id (182 rows), verified live.

select * from {{ ref('stg_fed_itis_taxon_unit_types__rank_types') }}
