{{ config(materialized='table', schema='ENVIRONMENT') }}

-- Built 2026-08-10 (backlog wave 4). PHMSA significant pipeline incidents — gas transmission & gathering systems only (other pipeline-type files are a follow-up), Jan 2010-present: one row per incident report (report_number unique) with operator identity (phmsa_operator_id is the operator join key), location, commodity, release volumes, fatality/injury counts, and status.
-- Grain: one row = one incident report. Curated core of the 624-column form; the full width stays in landing. Reads the staging model.

select * from {{ ref('stg_fed_phmsa_flagged_incidents__incidents') }}
