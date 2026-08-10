{{ config(materialized='table', schema='ENVIRONMENT') }}

-- Built 2026-08-10 (backlog wave 3). EPA RCRAInfo violations: one row = one violation record. Composite near-unique; provenance tiebreaker on the key (same violation type can be re-determined).
-- Reads the grain-verified staging model.

select * from {{ ref('stg_fed_epa_rcra_violations__violations') }}
