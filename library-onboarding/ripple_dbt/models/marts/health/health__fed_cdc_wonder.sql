{{ config(materialized='table', schema='HEALTH') }}

-- Rewritten 2026-08-09: the old version read the retired XML-capture raw shape
-- directly (its columns no longer exist). Builds on the staging model for the
-- relanded national mortality grid. Deaths NULL = CDC suppression (<10).
-- Grain: one row = year x ICD chapter x sex (national only, by CDC API policy;
-- state geography lives in health__fed_cdc_leading_causes_state).

select
    year,
    icd_chapter,
    sex,
    deaths,
    population,
    crude_rate,
    _ingested_at,
    _source_run_id
from {{ ref('stg_fed_cdc_wonder__records') }}
