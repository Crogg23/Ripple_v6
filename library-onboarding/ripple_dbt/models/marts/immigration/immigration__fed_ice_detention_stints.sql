{{ config(materialized='table', schema='IMMIGRATION') }}

-- Built 2026-08-09 (73-source backlog). ICE detention stints 2004-2026,
-- person-level (anonymized hashes). Excludes only the rows the publisher
-- explicitly flagged for dropping as duplicates; the softer duplicate_likely
-- flags are carried through for downstream judgment.
-- Grain: one row = one continuous hold at one facility.

select *
from {{ ref('stg_fed_ice_detention_stints__all') }}
where coalesce(duplicate_drop_row, 'False') <> 'True'
