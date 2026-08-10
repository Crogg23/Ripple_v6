{{ config(materialized='table', schema='ENERGY') }}

-- Built 2026-08-10 (backlog wave 4). EIA-861 annual electric utility survey, 2024 vintage.
-- EIA-861 (2024 vintage) Sales to Ultimate Customers - Customer Sited (community solar / facility-level): revenue (thousand dollars), sales (MWh) and customer counts by facility, utility, state and sector.
-- Grain: surrogate over (data_year, facility_number, utility_number, state); grain not verifiable pre-clean.

select * from {{ ref('stg_fed_eia861_sales_ult_cust_cs__facility_sales') }}
