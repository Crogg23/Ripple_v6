{{ config(materialized='table', schema='PROCUREMENT') }}

-- Built 2026-08-09 (73-source backlog, wave 2d). SAMPLE ONLY -- NOT the full dataset. USAspending subawards: a 5,000-row API slice of the multi-million-row subaward corpus, landed as flat JSON records. Use for shape/testing only.
-- Grain: one row = one subaward record (id unique in the slice).

select * from {{ ref('stg_fed_usaspending_subawards__subawards') }}
