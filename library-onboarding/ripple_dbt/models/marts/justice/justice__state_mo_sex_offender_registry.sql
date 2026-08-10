{{ config(materialized='table', schema='JUSTICE') }}

-- Built 2026-08-09 (73-source backlog, wave 2). Missouri public sex offender
-- registry (State Highway Patrol export).
-- Grain: one row = one registrant-offense.
-- Public-record compliance data; registry status (compliant flag, tier) is
-- the systemic lens, not the individuals.

select * from {{ ref('stg_state_mo_sex_offender_registry__offenses') }}
