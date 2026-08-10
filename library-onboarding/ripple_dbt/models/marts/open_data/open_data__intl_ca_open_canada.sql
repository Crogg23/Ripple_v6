{{ config(materialized='table', schema='OPEN_DATA') }}

-- Built 2026-08-09 (73-source backlog, wave 2d). SAMPLE ONLY -- NOT the full dataset. open.canada.ca dataset catalog: 500-dataset slice of the Canadian national open-data portal index.

select * from {{ ref('stg_intl_ca_open_canada__records') }}
