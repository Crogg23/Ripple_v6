{{ config(materialized='table', schema='ENVIRONMENT') }}

-- Built 2026-08-10 (backlog wave 3). EPA RCRAInfo enforcement actions with penalty amounts (proposed/final monetary penalties, supplemental project and cost-recovery amounts): one row = one enforcement record. Composite near-unique; provenance tiebreaker on the key.
-- Reads the grain-verified staging model.

select * from {{ ref('stg_fed_epa_rcra_enforcements__enforcements') }}
