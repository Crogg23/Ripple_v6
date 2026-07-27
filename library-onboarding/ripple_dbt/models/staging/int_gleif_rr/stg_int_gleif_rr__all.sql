    with source as (
        select * from {{ source('ripple_raw', 'INT_GLEIF_RR') }}
    )

    select
        "Relationship.StartNode.NodeID" as LEI,
"Relationship.EndNode.NodeID" as PARENT_LEI,
_INGESTED_AT,
_SOURCE_RUN_ID
    from source
    qualify row_number() over (
        partition by LEI
        order by _INGESTED_AT desc
    ) = 1
