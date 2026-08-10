{{ config(materialized='table', schema='ENERGY') }}

-- Built 2026-08-10 (backlog wave 4). EIA-861 annual electric utility survey, 2024 vintage.
-- EIA-861 (2024 vintage) Non-Net-Metering Distributed generators: distributed capacity (MW) by utility, state, interconnection type, customer sector, and technology group.
-- Grain: one row per utility per state per interconnection type (UTILITY_NUMBER+STATE+TYPE is near-unique: 495 distinct of 507 rows).

select * from {{ ref('stg_fed_eia861_non_net_metering_distributed__capacity') }}
