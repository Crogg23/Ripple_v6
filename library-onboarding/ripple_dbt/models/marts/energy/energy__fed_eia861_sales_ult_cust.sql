{{ config(materialized='table', schema='ENERGY') }}

-- Built 2026-08-10 (backlog wave 4). EIA-861 annual electric utility survey, 2024 vintage.
-- EIA-861 (2024 vintage) Sales to Ultimate Customers: revenue (thousand dollars), sales (MWh) and customer counts by utility, state, part, service type and customer sector.
-- Grain: surrogate over (data_year, utility_number, state, part, service_type); grain not verifiable pre-clean.

select * from {{ ref('stg_fed_eia861_sales_ult_cust__sales') }}
