{{ config(tags=['minimal_staging']) }}

-- GRAIN: one row per victim post — (post_title, group_name, discovered) is
-- unique (verified 2026-08-11 on the full pull). Re-pulled in full 2026-08-11
-- into XC_RANSOMWARELIVE_VICTIMS_FULL_R2 (30,661 rows). post_url is NOT a key:
-- publisher-side, 10,394 rows lack it and 469 URLs repeat.
-- Passthrough staging view: snake_case rename only, no dedup.

with source as (

    select * from {{ source('ripple_raw', 'XC_RANSOMWARELIVE_VICTIMS_FULL_R2') }}

),

renamed as (

    select
        POST_TITLE as post_title,
        GROUP_NAME as group_name,
        DISCOVERED as discovered,
        PUBLISHED as published,
        WEBSITE as website,
        COUNTRY as country,
        ACTIVITY as activity,
        DESCRIPTION as description,
        POST_URL as post_url,
        _INGESTED_AT as _loaded_at,
        'https://data.ransomware.live/victims.csv' as _source_url

    from source

)

select * from renamed
