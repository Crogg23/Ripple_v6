{{ config(materialized='table', schema='TRANSPORT') }}

-- Built 2026-08-09 (73-source backlog). FRA Form 55a rail casualties
-- (injuries/illnesses/deaths) 1975-present.
-- Grain: one row = one reported casualty (report_key unique).

select * from {{ ref('stg_fed_fra_casualties__all') }}
