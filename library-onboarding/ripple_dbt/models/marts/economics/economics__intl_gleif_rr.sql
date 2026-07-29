{{ config(materialized='table', schema='ECONOMICS') }}

-- GRAIN: one row per LEI relationship (child LEI → parent LEI)
-- Answers: Which legal entities own/control which other legal entities?
-- Source: GLEIF Relationship Records (~482K parent-child pairs)
-- Key joins: lei/parent_lei → intl_gleif (entity details)

with source as (
    select * from {{ source('ripple_raw', 'INT_GLEIF_RR') }}
)

select
    trim("Relationship.StartNode.NodeID")                as lei,
    trim("Relationship.EndNode.NodeID")                  as parent_lei,
    trim("Relationship.RelationshipType")                as relationship_type,
    trim("Relationship.RelationshipStatus")              as relationship_status,
    -- 2026-07-28 fix: raw values are ISO8601-with-timezone (e.g. '2012-11-29T00:00:00.000Z',
    -- '2011-10-01T00:00:00+02:00'), not bare 'YYYY-MM-DD' -- the old cast silently nulled
    -- every row (confirmed live: 0 of 391,664 populated). Date portion is always the first
    -- 10 chars regardless of timezone suffix.
    try_to_date(left(trim("Relationship.Period.1.startDate"), 10), 'YYYY-MM-DD') as period_start_date,
    try_to_date(left(trim("Relationship.Period.1.endDate"), 10), 'YYYY-MM-DD')   as period_end_date,
    (trim("Relationship.RelationshipStatus") = 'ACTIVE') as is_active,
    "_INGESTED_AT" as _loaded_at,
    "_SOURCE_RUN_ID" as _source_run_id
from source
qualify row_number() over (
    partition by "Relationship.StartNode.NodeID", "Relationship.EndNode.NodeID"
    order by "_INGESTED_AT" desc
) = 1
