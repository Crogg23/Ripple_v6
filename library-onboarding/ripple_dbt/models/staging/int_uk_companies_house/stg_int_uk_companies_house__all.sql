    with source as (
        select * from {{ source('ripple_raw', 'INT_UK_COMPANIES_HOUSE') }}
    )

    select
        "CompanyNumber" as UK_COMPANY_NUMBER,
_INGESTED_AT,
_SOURCE_RUN_ID
    from source
    qualify row_number() over (
        partition by UK_COMPANY_NUMBER
        order by _INGESTED_AT desc
    ) = 1
