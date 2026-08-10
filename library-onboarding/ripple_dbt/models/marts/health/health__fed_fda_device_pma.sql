{{ config(materialized='table', schema='HEALTH') }}

-- Built 2026-08-09 (73-source backlog, wave 2d). FDA PMA premarket approvals: 56.9k approval/supplement records flattened from raw openFDA JSON -- effectively the full corpus.

select * from {{ ref('stg_fed_fda_device_pma__all') }}
