{{ config(materialized='table', schema='SCIENCE_RESEARCH') }}

-- Built 2026-08-10 (backlog wave 4). Federal SBIR/STTR small-business research awards with UEI and DUNS company join keys.
-- Grain: one row = one award record (surrogate-keyed; 127 composite collisions tiebroken deterministically).

select * from {{ ref('stg_fed_sbir_sttr_awards__awards') }}
