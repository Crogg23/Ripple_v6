{{ config(materialized='table', schema='POLITICS') }}

-- Built 2026-08-09 (73-source backlog, wave 2d). SAMPLE ONLY -- NOT the full dataset. FEC itemized contributions API: a 500-row default-page slice. Use for shape/testing only; the FEC bulk files are the real corpus (separate sources).

select * from {{ ref('stg_fed_fec_api__records') }}
