    with source as (
        select * from {{ source('ripple_raw', 'FED_CMS_PARTB_PROVIDER_DY2018') }}
    )

    select
        "Rndrng_NPI" as NPI,
_INGESTED_AT,
_SOURCE_RUN_ID
    from source
    qualify row_number() over (
        partition by NPI
        order by _INGESTED_AT desc
    ) = 1
