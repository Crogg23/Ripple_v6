{{ config(materialized='table', schema='ENVIRONMENT') }}

-- Built 2026-08-10 (73-source backlog, wave 3). USCG National Response Center
-- incident reports — pollution/spill/chemical release calls (1.03M rows).
-- Grain: one row = one incident report (seqnos unique). This is the primary
-- NRC source; a smaller sibling extract with unlabeled trailing columns is
-- modeled separately.
-- The harm lens: which companies keep showing up as the responsible party.

select * from {{ ref('stg_fed_uscg_nrc_incidents__incidents') }}
