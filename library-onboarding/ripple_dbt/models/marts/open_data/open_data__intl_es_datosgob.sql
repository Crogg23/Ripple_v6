{{ config(materialized='table', schema='OPEN_DATA') }}

-- Built 2026-08-09 (73-source backlog, wave 2d). SAMPLE ONLY -- NOT the full dataset. datos.gob.es dataset catalog: 1,000-row slice AND defective as landed -- URI/title/description columns are blank (loader parse bug, needs a re-point); publisher/sector/format/URL populated.

select * from {{ ref('stg_intl_es_datosgob__records') }}
