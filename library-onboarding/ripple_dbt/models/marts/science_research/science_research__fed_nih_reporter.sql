{{ config(materialized='table', schema='SCIENCE_RESEARCH') }}

-- Built 2026-08-09 (73-source backlog, wave 2). NIH RePORTER grant projects,
-- full FY2000-FY2026 crawl (~2M applications).
-- Grain: one row = one application (appl_id unique).
-- Key joins: ORG_UEI/ORG_DUNS -> spending/registry sources; PI profile ids.

select * from {{ ref('stg_fed_nih_reporter__projects') }}
