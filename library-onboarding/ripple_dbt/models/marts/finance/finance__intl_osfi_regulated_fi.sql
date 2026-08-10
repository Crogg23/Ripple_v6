{{ config(materialized='table', schema='FINANCE') }}

-- Built 2026-08-10 (backlog wave 4). Canadian OSFI-regulated financial institutions register.
-- Grain: one row = one regulated-institution record (osfi_fi_record_id). Reads the staging model built alongside it.

select * from {{ ref('stg_intl_osfi_regulated_fi__institutions') }}
