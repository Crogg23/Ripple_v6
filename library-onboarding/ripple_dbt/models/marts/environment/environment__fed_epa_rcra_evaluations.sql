{{ config(materialized='table', schema='ENVIRONMENT') }}

-- Built 2026-08-10 (backlog wave 3). EPA RCRAInfo compliance evaluations (inspections): one row = one evaluation record. Composite near-unique; provenance tiebreaker on the key (multiple agency rows can share an identifier).
-- Reads the grain-verified staging model.

select * from {{ ref('stg_fed_epa_rcra_evaluations__evaluations') }}
