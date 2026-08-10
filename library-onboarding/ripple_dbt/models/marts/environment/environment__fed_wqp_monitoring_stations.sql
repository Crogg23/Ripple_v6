{{ config(materialized='table', schema='ENVIRONMENT') }}

-- Built 2026-08-10 (backlog wave 4). Water Quality Portal monitoring stations; huceightdigitcode joins to USGS watershed (WBD HUC8) data.
-- Grain: one row = one monitoring station (monitoringlocationidentifier unique). Reads the staging model built alongside it.

select * from {{ ref('stg_fed_wqp_monitoring_stations__stations') }}
