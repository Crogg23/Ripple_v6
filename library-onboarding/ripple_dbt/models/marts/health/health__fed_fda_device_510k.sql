{{ config(materialized='table', schema='HEALTH') }}

-- Built 2026-08-09 (73-source backlog, wave 2d). FDA 510(k) premarket clearances: 175.7k clearance records flattened from raw openFDA JSON -- effectively the full corpus.

select * from {{ ref('stg_fed_fda_device_510k__all') }}
