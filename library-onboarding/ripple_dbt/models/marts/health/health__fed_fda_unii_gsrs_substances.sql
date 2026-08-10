{{ config(materialized='table', schema='HEALTH') }}

-- Built 2026-08-10 (backlog wave 4). FDA GSRS substance registry: UNII codes with crosswalks to CAS RN, RXCUI, PubChem, InChIKey and more — a join-key hub for chemical/drug substance linkage.
-- Grain: one row = one substance (UNII exactly unique).

select * from {{ ref('stg_fed_fda_unii_gsrs_substances__substances') }}
