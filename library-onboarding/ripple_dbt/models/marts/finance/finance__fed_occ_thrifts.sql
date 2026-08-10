{{ config(materialized='table', schema='FINANCE') }}

-- Built 2026-08-10 (backlog wave 4). OCC federal thrifts; cert joins to FDIC data, rssd joins to FFIEC/Fed data. Junk trailing columns COL7/COL8/COL9 (all null artifacts of the source spreadsheet) are dropped in staging.
-- Grain: one row = one OCC-regulated federal thrift (charter_no unique). Reads the staging model built alongside it.

select * from {{ ref('stg_fed_occ_thrifts__thrifts') }}
