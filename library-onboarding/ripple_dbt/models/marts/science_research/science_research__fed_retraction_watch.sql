{{ config(materialized='table', schema='SCIENCE_RESEARCH') }}

-- Built 2026-08-09 (73-source backlog, wave 2). Retraction Watch database.
-- Grain: one row = one retraction/correction record.
-- Key joins: DOI / PubMed id -> publication corpora; institution names.

select * from {{ ref('stg_fed_retraction_watch__retractions') }}
