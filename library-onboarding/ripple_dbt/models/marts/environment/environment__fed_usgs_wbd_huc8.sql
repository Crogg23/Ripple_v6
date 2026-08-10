{{ config(materialized='table', schema='ENVIRONMENT') }}

-- Built 2026-08-10 (backlog wave 4). USGS Watershed Boundary Dataset HUC-8
-- subbasin index: names, states touched, areas, and source lineage.
-- Grain: one row = one 8-digit hydrologic unit (huc8 unique, 2,456 rows).
-- huc8 joins environmental datasets keyed by hydrologic unit.

select * from {{ ref('stg_fed_usgs_wbd_huc8__watersheds') }}
