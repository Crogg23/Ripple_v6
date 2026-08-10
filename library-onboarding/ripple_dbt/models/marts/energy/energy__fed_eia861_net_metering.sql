{{ config(materialized='table', schema='ENERGY') }}

-- Built 2026-08-10 (backlog wave 4). EIA-861 annual electric utility survey, 2024 vintage.
-- EIA-861 (2024 vintage) Net Metering: net-metered capacity (MW), installations, energy sold back (MWh), virtual/community capacity and PV-paired battery storage, by utility, state, technology type and customer sector.
-- Grain: surrogate over (data_year, utility_number, state, technology_type); grain not verifiable pre-clean.

select * from {{ ref('stg_fed_eia861_net_metering__capacity') }}
