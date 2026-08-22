{{ config(materialized='table', schema='REFERENCE') }}

-- GRAIN: one row per Census cartographic boundary shape (state, 500k resolution)
-- Loaded 2026-08-22 (scripts/census_boundaries_load.py) -- the warehouse's
-- first polygon layer; the Laboratory sweep found zero polygon columns before
-- this. GEOMETRY is a real GEOGRAPHY (WKT parsed with try_to_geography so a
-- malformed shape nulls instead of killing the build).

select
    * exclude (GEOMETRY_WKT),
    try_to_geography(GEOMETRY_WKT) as GEOMETRY
from {{ source('ripple_raw', 'XC_CENSUS_CB_STATE') }}
