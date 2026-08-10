{{ config(materialized='table', schema='OPEN_DATA') }}

-- Built 2026-08-09 (73-source backlog, wave 2d). SAMPLE ONLY -- NOT the full dataset. data.gov.gr dataset catalog: 5,000-row slice; 12 dataset ids appear twice as published.

select * from {{ ref('stg_intl_gr_datagov__records') }}
