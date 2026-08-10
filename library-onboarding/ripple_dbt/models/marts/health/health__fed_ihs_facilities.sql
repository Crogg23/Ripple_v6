{{ config(materialized='table', schema='HEALTH') }}

-- Built 2026-08-10 (backlog wave 4). IHS / Tribal / Urban Indian Health
-- facilities list (June 2023 release) with address, service flags, workload,
-- ownership/operation, and coordinates. Preamble/title/header rows that the
-- loader embedded as data are filtered out in staging (numeric-ASUFAC filter),
-- and columns are renamed positionally onto the real embedded header.
-- Grain: ihs_facility_id (surrogate over asufac + modifier).

select * from {{ ref('stg_fed_ihs_facilities__facilities') }}
