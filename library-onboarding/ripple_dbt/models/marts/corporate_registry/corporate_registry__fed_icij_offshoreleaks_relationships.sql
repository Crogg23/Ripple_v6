{{ config(materialized='table', schema='CORPORATE_REGISTRY') }}

-- Built 2026-08-09 (73-source backlog). ICIJ Offshore Leaks graph edges.
-- Grain: one row = one edge as published; (start, end, type, link) NOT
-- unique (multi-leak republication) — kept as landed, no dedup.

select * from {{ ref('stg_fed_icij_offshoreleaks__relationships') }}
