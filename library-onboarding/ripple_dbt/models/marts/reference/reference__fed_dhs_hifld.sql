{{ config(materialized='table', schema='REFERENCE') }}

-- Built 2026-08-09 (73-source backlog, wave 2d). SAMPLE ONLY -- NOT the full dataset. DHS HIFLD infrastructure facilities: a 500-row slice of one layer. objectid+layer unique in the slice. Use for shape/testing only.
-- Grain: one row = one facility in the sampled layer.

select * from {{ ref('stg_fed_dhs_hifld__facilities') }}
