{{ config(materialized='table', schema='OPEN_DATA') }}

-- Built 2026-08-09 (73-source backlog, wave 2d). SAMPLE ONLY -- NOT the full dataset. GovData.de dataset catalog: 5,000-dataset slice of the German national open-data portal index.

select * from {{ ref('stg_intl_de_govdata__records') }}
