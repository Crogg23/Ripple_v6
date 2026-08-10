{{ config(materialized='table', schema='HEALTH') }}

-- Built 2026-08-10 (backlog wave 4). NLM DailyMed SPL set-id to label file map: zip file, upload date, version, and title per drug label set id.
-- Grain: one row = one SPL set id (SETID exactly unique).

select * from {{ ref('stg_fed_nlm_dailymed_spl_setid_map__setid_map') }}
