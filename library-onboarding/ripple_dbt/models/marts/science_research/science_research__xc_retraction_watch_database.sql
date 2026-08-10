{{ config(materialized='table', schema='SCIENCE_RESEARCH') }}

-- Built 2026-08-10 (backlog wave 4). Retraction Watch database: retracted /
-- corrected papers with DOIs, retraction reasons, institutions, journals.
-- Grain: one row = one retraction record, unique on the surrogate
-- retraction_record_id (RECORD_ID is near-unique: 71,389 distinct of 71,608).
-- Key joins: original/retraction DOI and PubMed ids -> publication corpora.

select * from {{ ref('stg_xc_retraction_watch_database__retractions') }}
