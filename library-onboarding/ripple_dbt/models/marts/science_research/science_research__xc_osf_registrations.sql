{{ config(materialized='table', schema='SCIENCE_RESEARCH') }}

-- SAMPLE ONLY -- NOT the full dataset: 10-row proof slice of the much larger
-- OSF (Open Science Framework) registrations registry.
-- Built 2026-08-10 (backlog wave 4). Preregistrations with titles, dates,
-- registration-state flags, and relationship ids into the OSF graph.
-- Grain: one row = one registration (osf_id unique). Curated column subset;
-- the 370-column raw width stays in the landing table.

select * from {{ ref('stg_xc_osf_registrations__registrations') }}
