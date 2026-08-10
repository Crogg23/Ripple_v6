{{ config(materialized='table', schema='REFERENCE') }}

-- Built 2026-08-10 (backlog wave 4). ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.
-- Taxonomic experts cited as evidence sources; one row per expert id (with prefix).
-- Grain: one row per expert_id_prefix, expert_id (197 rows), verified live.

select * from {{ ref('stg_fed_itis_experts__experts') }}
