{{ config(materialized='table', schema='ENVIRONMENT') }}

-- Built 2026-08-10 (backlog wave 4). USGS orphaned oil & gas wells; well_identifier is usually an API well number, joinable to state well registries.
-- Grain: one row = one orphaned well record (well_record_id). Reads the staging model built alongside it.

select * from {{ ref('stg_fed_usgs_orphaned_oil_gas_wells__wells') }}
