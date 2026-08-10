{{ config(materialized='table', schema='FINANCE') }}

-- Built 2026-08-10 (backlog wave 4). FINRA market-participant IDs (MPIDs) with venue membership flags.
-- Grain: one row = one MPID registration record (mpid_record_id). Reads the staging model built alongside it.

select * from {{ ref('stg_fed_finra_mpid_list__market_participants') }}
