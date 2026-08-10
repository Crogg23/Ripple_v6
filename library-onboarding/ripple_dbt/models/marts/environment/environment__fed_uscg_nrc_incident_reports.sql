{{ config(materialized='table', schema='ENVIRONMENT') }}

-- Built 2026-08-10 (73-source backlog, wave 3). Secondary USCG National
-- Response Center extract (116,662 rows). Grain: one row = one incident
-- report (seqnos unique). Same NRC feed as the primary million-row source,
-- but this extract's trailing payload columns arrived unlabeled from the
-- publisher (kept as extra_col_1..5).

select * from {{ ref('stg_fed_uscg_nrc_incident_reports__incident_reports') }}
