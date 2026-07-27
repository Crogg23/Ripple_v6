    with source as (
        select * from {{ source('ripple_raw', 'FED_EPA_FRS_FULL') }}
    )

    select
        "REGISTRY_ID" as FRS_ID,
"FEDERAL_FACILITY_CODE_EIN" as EIN,
_INGESTED_AT,
_SOURCE_RUN_ID
    from source
    qualify row_number() over (
        partition by FRS_ID
        order by _INGESTED_AT desc
    ) = 1
