{{ config(materialized='table', schema='POLITICS') }}

-- Built 2026-08-09 (73-source backlog, wave 2b). IRS Form 8871 directors & officers of Section 527 political organizations: one row per listed person per form (form_id + director_id unique).
-- Grain: one row = one director/officer listing.

select * from {{ ref('stg_irs527__directors_officers') }}
