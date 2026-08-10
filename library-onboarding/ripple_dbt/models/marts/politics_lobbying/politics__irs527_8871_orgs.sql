{{ config(materialized='table', schema='POLITICS') }}

-- Built 2026-08-09 (73-source backlog, wave 2b). IRS Form 8871 notices: Section 527 political organizations' registration filings (form_id_number unique).
-- Grain: one row = one Form 8871 filing. Reads the pre-existing staging model.

select * from {{ ref('stg_irs527_8871_orgs__registrations') }}
