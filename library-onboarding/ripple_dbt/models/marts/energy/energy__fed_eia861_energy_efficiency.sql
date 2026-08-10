{{ config(materialized='table', schema='ENERGY') }}

-- Built 2026-08-10 (backlog wave 4). EIA-861 annual electric utility survey, 2024 vintage.
-- EIA-861 (2024 vintage) Energy Efficiency: incremental and life-cycle energy savings (MWh), peak demand savings (MW), customer incentives and other costs (thousand dollars) by utility, state and sector.
-- Grain: surrogate over (data_year, utility_number, state); grain not verifiable pre-clean.

select * from {{ ref('stg_fed_eia861_energy_efficiency__programs') }}
