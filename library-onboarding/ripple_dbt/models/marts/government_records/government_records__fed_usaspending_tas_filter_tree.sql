{{ config(materialized='table', schema='GOVERNMENT_RECORDS') }}

-- Built 2026-08-10 (backlog wave 4). USAspending Treasury Account Symbol (TAS)
-- filter tree: agency-level nodes with federal-account counts. ANCESTORS is a
-- VARIANT array passed through from landing.
-- Grain: one row = one tree node (node_id unique, 92 rows).

select * from {{ ref('stg_fed_usaspending_tas_filter_tree__tas_nodes') }}
