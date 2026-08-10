{{ config(materialized='table', schema='HEALTH') }}

-- Built 2026-08-09 (73-source backlog, wave 2d). FDA MAUDE device adverse-event reports, device-level grain, 2.74M rows flattened from raw openFDA JSON. Scope: 2020Q1-forward slice of the 1993-2026 history (documented in staging).

select * from {{ ref('stg_fed_fda_maude__all') }}
