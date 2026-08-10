{{ config(materialized='table', schema='HEALTH') }}

-- Built 2026-08-09 (73-source backlog, wave 2d). FDA Global UDI Database (GUDID): 5.08M device records flattened from raw openFDA JSON pages -- effectively the full corpus.

select * from {{ ref('stg_fed_fda_gudid__all') }}
