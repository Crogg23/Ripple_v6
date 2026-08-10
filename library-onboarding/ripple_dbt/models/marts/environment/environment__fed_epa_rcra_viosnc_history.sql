{{ config(materialized='table', schema='ENVIRONMENT') }}

-- Built 2026-08-10 (backlog wave 3). EPA RCRAInfo violation / significant-non-compliance monthly history: one row = one handler-location-month status (vio_flag / snc_flag).
-- Reads the grain-verified staging model.

select * from {{ ref('stg_fed_epa_rcra_viosnc_history__monthly_status') }}
