{{ config(materialized='table', schema='FINANCE') }}

-- Built 2026-08-10 (backlog wave 4). ISO 10383 market identifier codes (trading venues); lei joins to GLEIF LEI data.
-- Grain: one row = one market identifier code (mic unique). Reads the staging model built alongside it.

select * from {{ ref('stg_intl_iso_mic_registry__market_identifier_codes') }}
