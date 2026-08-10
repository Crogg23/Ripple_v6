{{ config(materialized='table', schema='POLITICS') }}

-- Built 2026-08-09 (73-source backlog, wave 2b). IRS Form 8871 related entities of 527 orgs: one row per related entity per form (form_id + entity_id unique).
-- Grain: one row = one related-entity listing.

select * from {{ ref('stg_irs527__related_entities') }}
