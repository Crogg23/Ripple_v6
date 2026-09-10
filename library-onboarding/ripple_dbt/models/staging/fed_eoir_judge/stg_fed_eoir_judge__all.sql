    with source as (
        select * from {{ source('ripple_raw', 'FED_EOIR_JUDGE') }}
    )

    select
        "IDNJUDGE",
"JUDGE_CODE" as JUDGE_CODE,
"JUDGE_NAME",
"JUDGE_ST_ADDRESS",
"JUDGE_CITY",
"JUDGE_STATE",
"JUDGE_ZIP_1",
"JUDGE_ZIP_2",
"JUDGE_PHONE_NO",
"DATCREATEDON",
"DATMODIFIEDON",
"BLNACTIVE",
"BLNSKIPPEDONWHEEL",
"BLNLASTONWHEEL",
"BLNSKIPPEDONWHEELMA",
"BLNLASTONWHEELMA",
"INTORDERMA",
"INTORDERMM",
_INGESTED_AT,
_SOURCE_RUN_ID
    from source
    qualify row_number() over (
        partition by JUDGE_CODE
        order by _INGESTED_AT desc
    ) = 1
