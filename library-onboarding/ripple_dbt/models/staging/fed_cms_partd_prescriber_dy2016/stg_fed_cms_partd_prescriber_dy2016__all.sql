    with source as (
        select * from {{ source('ripple_raw', 'FED_CMS_PARTD_PRESCRIBER_DY2016') }}
    )

    select
        "Prscrbr_NPI" as NPI,
_INGESTED_AT,
_SOURCE_RUN_ID
    from source
    qualify row_number() over (
        partition by NPI
        order by _INGESTED_AT desc
    ) = 1
