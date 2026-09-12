    with source as (
        select * from {{ source('ripple_raw', 'FED_SEC_13F_SECURITIES_LIST') }}
    )

    select
        "LINE_NO",
"CUSIP" as CUSIP,
"HAS_LISTED_OPTIONS",
"ISSUER_NAME",
"ISSUER_DESCRIPTION",
"STATUS",
"LIST_QUARTER",
_INGESTED_AT,
_SOURCE_RUN_ID
    from source
    qualify row_number() over (
        partition by CUSIP
        order by _INGESTED_AT desc
    ) = 1
