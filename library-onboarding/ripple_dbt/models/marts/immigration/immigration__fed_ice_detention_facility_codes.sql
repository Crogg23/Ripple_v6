{{ config(materialized='table', schema='IMMIGRATION') }}

-- Built 2026-08-10 (backlog wave 4). ICE detention facility codes with lat/long; detention_facility_code is the join key into ICE detention stint/detainer data.
-- Grain: one row = one detention facility code (detention_facility_code unique). Reads the staging model built alongside it.

select * from {{ ref('stg_fed_ice_detention_facility_codes__facility_codes') }}
