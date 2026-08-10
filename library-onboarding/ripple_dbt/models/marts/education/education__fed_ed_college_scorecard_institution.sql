{{ config(materialized='table', schema='EDUCATION') }}

-- Built 2026-08-10 (backlog wave 4). Dept. of Education College Scorecard,
-- institution-level file. Staging keeps a curated ~60-column core (identity,
-- location, control, admissions, enrollment, costs, completion, earnings,
-- debt, default/repayment); the full 3,311-column width stays in landing.
-- Grain: one row = one institution (unitid unique, 6,273 rows).

select * from {{ ref('stg_fed_ed_college_scorecard_institution__institutions') }}
