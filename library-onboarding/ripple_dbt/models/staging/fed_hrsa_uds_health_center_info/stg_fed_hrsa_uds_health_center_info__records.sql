{{ config(tags=['minimal_staging']) }}

-- GRAIN: NOT YET DETERMINED (passthrough -- needs manual review before mart use)
-- This is a passthrough staging view: select * from the raw landing table, no
-- dedup, no renaming (source columns already came in snake_case-able as-is).
-- Written by hand for the 2026-08-05 housing/health ingestion phase.

with source as (

    select * from {{ source('ripple_raw', 'FED_HRSA_UDS_HEALTH_CENTER_INFO') }}

),

renamed as (

    select
        *,
        _INGESTED_AT as _loaded_at,
        'https://data.hrsa.gov/topics/health-centers/uds' as _source_url

    from source

)

select * from renamed
