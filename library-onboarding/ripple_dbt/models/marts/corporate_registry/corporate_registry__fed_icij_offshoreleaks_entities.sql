{{ config(materialized='table', schema='CORPORATE_REGISTRY') }}

-- Built 2026-08-09 (73-source backlog). ICIJ Offshore Leaks entity nodes.
-- Grain: one row = one offshore entity (node_id unique).

select * from {{ ref('stg_fed_icij_offshoreleaks__entities') }}
