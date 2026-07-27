    with source as (
        select * from {{ source('ripple_raw', 'FED_SEC_13F_SUBMISSION') }}
    )

    select
        "CIK" as CIK,
_INGESTED_AT,
_SOURCE_RUN_ID
    from source
    qualify row_number() over (
        partition by CIK
        order by _INGESTED_AT desc
    ) = 1
