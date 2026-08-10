{{ config(materialized='table', schema='POLITICS') }}

-- Built 2026-08-09 (73-source backlog, wave 2b). Texas lobby docket/proceeding designations: one row per docket line (lobbydocketdesigid unique).
-- Grain: one row = one docket line.

select * from {{ ref('stg_tx_lobby__dockets') }}
