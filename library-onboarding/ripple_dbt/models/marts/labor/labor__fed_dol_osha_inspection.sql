{{ config(materialized='table', enabled=false, schema='LABOR') }}
-- DISABLED: source table FED_DOL_OSHA_INSPECTION does not exist in LANDING
select 1 as _placeholder
