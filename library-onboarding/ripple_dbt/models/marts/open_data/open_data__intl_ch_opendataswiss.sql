{{ config(materialized='table', schema='OPEN_DATA') }}

-- Built 2026-08-09 (73-source backlog, wave 2d). SAMPLE ONLY -- NOT the full dataset. opendata.swiss dataset catalog: 5,000-dataset slice of the Swiss national open-data portal index.

select * from {{ ref('stg_intl_ch_opendataswiss__records') }}
