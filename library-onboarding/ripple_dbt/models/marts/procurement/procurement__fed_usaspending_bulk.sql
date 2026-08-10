{{ config(materialized='table', schema='PROCUREMENT') }}

-- Built 2026-08-09 (73-source backlog, wave 2d). SAMPLE ONLY -- NOT the full dataset. USAspending prime-award contract transactions: a 50,000-row slice of a multi-hundred-million-row corpus (bulk loader capped). Use for shape/testing, never for totals or coverage claims. Full re-ingest needs a dedicated streaming loader.

select * from {{ ref('stg_fed_usaspending_bulk__organizations') }}
