{{ config(materialized='table', schema='POLITICS') }}

-- Built 2026-08-09 (73-source backlog, wave 2b). CAL-ACCESS lobbying cover-page entity lines: one row per entity line item on a filing version (filing_id + amend_id + line_item unique).
-- Grain: one row = one entity line on a filing version.

select * from {{ ref('stg_ca_lobby__cover2') }}
