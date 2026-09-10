    with source as (
        select * from {{ source('ripple_raw', 'FED_CMS_NPPES_DEACTIVATED') }}
    )

    select
        "NPI" as NPI,
"NPPES_DEACTIVATION_DATE",
_INGESTED_AT,
_SOURCE_RUN_ID
    from source
    qualify row_number() over (
        partition by NPI
        order by _INGESTED_AT desc
    ) = 1
