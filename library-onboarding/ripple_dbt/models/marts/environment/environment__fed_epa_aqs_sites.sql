{{ config(materialized='table', schema='ENVIRONMENT') }}

-- Built 2026-08-10 (backlog wave 4). EPA AQS air-quality monitoring sites; aqs_site_id = state-county-site composite, FIPS pieces join to census geography.
-- Grain: one row = one monitoring site (state_code + county_code + site_number exactly unique). Reads the staging model built alongside it.

select * from {{ ref('stg_fed_epa_aqs_sites__sites') }}
