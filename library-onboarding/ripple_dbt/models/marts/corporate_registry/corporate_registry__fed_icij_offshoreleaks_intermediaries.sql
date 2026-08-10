{{ config(materialized='table', schema='CORPORATE_REGISTRY') }}

-- Built 2026-08-09 (73-source backlog). ICIJ Offshore Leaks intermediary
-- nodes (law firms, banks, agents). Grain: one row = one intermediary.

select * from {{ ref('stg_fed_icij_offshoreleaks__intermediaries') }}
