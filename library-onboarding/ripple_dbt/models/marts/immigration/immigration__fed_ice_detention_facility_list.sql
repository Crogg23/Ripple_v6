{{ config(materialized='table', schema='IMMIGRATION') }}

-- Built 2026-08-09 (73-source backlog, wave 2c). ICE detention facility list (facility name, city/state, AOR, detailed type). One published duplicate name+city pair kept as landed.
-- Grain: one row = one facility listing. Reads the pre-existing staging model.

select * from {{ ref('stg_fed_ice_detention_facility_list__facility') }}
