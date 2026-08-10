{{ config(materialized='table', schema='ENVIRONMENT') }}

-- Built 2026-08-10 (73-source backlog, wave 3). FracFocus hydraulic-fracturing
-- chemical disclosure registry, full ingredient-level extract (7.2M rows).
-- Grain: one row = one ingredient line within a purpose within a well
-- disclosure (surrogate key ingredient_record_id over disclosure/purpose/
-- ingredient IDs, verified exactly unique).
-- The harm lens: which chemicals (CAS numbers, trade-secret masking) go into
-- the ground, where, by which operator.

select * from {{ ref('stg_fed_fracfocus_registry__ingredients') }}
