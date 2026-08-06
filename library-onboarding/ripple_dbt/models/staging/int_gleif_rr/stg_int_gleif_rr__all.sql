    -- GRAIN: one row per (LEI, PARENT_LEI, RELATIONSHIP_TYPE).
    -- Fix: dedup was LEI-only and dropped RELATIONSHIP_TYPE entirely, collapsing
    -- 481,933 relationship rows to one per child LEI (182,433 rows / 38% lost).
    -- A child LEI legitimately carries multiple relationship rows -- e.g. a
    -- separate row for IS_DIRECTLY_CONSOLIDATED_BY vs IS_ULTIMATELY_CONSOLIDATED_BY.
    -- Raw table has zero exact-duplicate ingests on this triplet as of 2026-08-05,
    -- so the qualify below only protects against future re-ingests.
    with source as (
        select * from {{ source('ripple_raw', 'INT_GLEIF_RR') }}
    )

    select
        "Relationship.StartNode.NodeID" as LEI,
"Relationship.EndNode.NodeID" as PARENT_LEI,
"Relationship.RelationshipType" as RELATIONSHIP_TYPE,
_INGESTED_AT,
_SOURCE_RUN_ID
    from source
    qualify row_number() over (
        partition by LEI, PARENT_LEI, RELATIONSHIP_TYPE
        order by _INGESTED_AT desc
    ) = 1
