{{ config(materialized='table', schema='POLITICS') }}

-- Built 2026-08-09 (73-source backlog, wave 2b). CAL-ACCESS lobbying registration amendments (Form 605): one row per amendment filing version (filing_id + amend_id unique).
-- Grain: one row = one amendment filing version.

select * from {{ ref('stg_ca_lobby__amendments') }}
