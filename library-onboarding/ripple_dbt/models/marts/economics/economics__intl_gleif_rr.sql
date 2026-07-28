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
    try_to_date(trim("Relationship.Period.1.startDate"), 'YYYY-MM-DD') as period_start_date,
    try_to_date(trim("Relationship.Period.1.endDate"), 'YYYY-MM-DD')   as period_end_date,
    (trim("Relationship.RelationshipStatus") = 'ACTIVE') as is_active,
    "_INGESTED_AT" as _loaded_at,
    "_SOURCE_RUN_ID" as _source_run_id
from source
qualify row_number() over (
    partition by "Relationship.StartNode.NodeID", "Relationship.EndNode.NodeID"
    order by "_INGESTED_AT" desc
) = 1
