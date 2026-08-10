{{ config(materialized='table', schema='ENVIRONMENT') }}

-- Built 2026-08-10 (backlog wave 3). EPA RCRAInfo hazardous-waste handler universe: one row = one RCRA handler (ID_NUMBER unique). Name, address, enforcement universe flags, generator status.
-- Reads the grain-verified staging model.

select * from {{ ref('stg_fed_epa_rcra_facilities__facilities') }}
