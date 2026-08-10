{{ config(materialized='table', schema='CORPORATE_REGISTRY') }}

-- Built 2026-08-10 (73-source backlog, wave 3). SAMPLE ONLY -- NOT the full dataset: ~7.0M of ~10M PSC records from the 2026-08-05 UK Companies House "Persons with Significant Control" snapshot; the load truncated mid-stream (single provenance batch), so this is truncation, not random sampling. Full reload queued.
-- Grain: one row = one PSC record, unique on psc_link_self. company_number joins to the already-modeled UK company register.

select * from {{ ref('stg_uk_companies_house_psc__psc_records') }}
