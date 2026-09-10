    with source as (
        select * from {{ source('ripple_raw', 'FED_CMS_SNF_OWNERSHIP') }}
    )

    select
        "ENROLLMENT ID" as ENROLLMENT_ID,
_INGESTED_AT,
_SOURCE_RUN_ID
    from source
    qualify row_number() over (
        partition by ENROLLMENT_ID
        order by _INGESTED_AT desc
    ) = 1
