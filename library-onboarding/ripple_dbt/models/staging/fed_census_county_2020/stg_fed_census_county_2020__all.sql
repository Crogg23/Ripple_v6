    with source as (
        select * from {{ source('ripple_raw', 'FED_CENSUS_COUNTY_2020') }}
    )

    select
        "STATE",
"STATEFP",
"COUNTYFP",
"COUNTYNS" as COUNTYNS,
"COUNTYNAME",
"CLASSFP",
"FUNCSTAT",
_INGESTED_AT,
_SOURCE_RUN_ID
    from source
    qualify row_number() over (
        partition by COUNTYNS
        order by _INGESTED_AT desc
    ) = 1
