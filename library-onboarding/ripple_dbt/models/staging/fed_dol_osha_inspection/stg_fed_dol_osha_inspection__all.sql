    with source as (
        select * from {{ source('ripple_raw', 'FED_DOL_OSHA_INSPECTION') }}
    )

    select
        "activity_nr" as OSHA_ACTIVITY_NR,
_INGESTED_AT,
_SOURCE_RUN_ID
    from source
    qualify row_number() over (
        partition by OSHA_ACTIVITY_NR
        order by _INGESTED_AT desc
    ) = 1
