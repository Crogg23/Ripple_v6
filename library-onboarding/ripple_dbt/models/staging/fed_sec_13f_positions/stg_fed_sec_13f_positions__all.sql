    with source as (
        select * from {{ source('ripple_raw', 'FED_SEC_13F_POSITIONS') }}
    )

    select
        "CUSIP" as CUSIP,
"ACCESSION_NUMBER" as SEC_ACCESSION_NUMBER,
_INGESTED_AT,
_SOURCE_RUN_ID
    from source
    qualify row_number() over (
        partition by CUSIP
        order by _INGESTED_AT desc
    ) = 1
