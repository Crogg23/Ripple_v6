    with source as (
        select * from {{ source('ripple_raw', 'FED_EPA_FRS_FULL') }}
    )

    select
        "REGISTRY_ID" as FRS_ID,
-- NOTE: an earlier version selected "FEDERAL_FACILITY_CODE_EIN" as EIN, but the
-- landing table has no EIN column at all. FEDERAL_FACILITY_CODE is a Yes/blank
-- federal-facility flag, not an identifier, so no EIN is exposed here.
_INGESTED_AT,
_SOURCE_RUN_ID
    from source
    qualify row_number() over (
        partition by FRS_ID
        order by _INGESTED_AT desc
    ) = 1
