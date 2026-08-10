{{ config(materialized='table', schema='OPEN_DATA') }}

-- Built 2026-08-09 (73-source backlog, wave 2d). SAMPLE ONLY -- NOT the full dataset. datos.gob.cl dataset catalog: 1,000-dataset slice of the Chilean national open-data portal index.

select * from {{ ref('stg_intl_cl_datosgob__records') }}
