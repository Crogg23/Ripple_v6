{{ config(tags=['spine_generated']) }}

-- GRAIN: one row per DATASET (dataset_id unique; slug also unique).
-- Re-pulled in full 2026-08-11 into INTL_FR_DATA_GOUV_FULL (130,431 rows).
-- SCHEMA CHANGE: the full publisher export is DATASET-grain, not
-- dataset+resource grain like the old capped table. Resource-level columns
-- (RESOURCE_ID, RESOURCE_TITLE, RESOURCE_URL, ...) no longer exist; the new
-- export instead carries owner, harvest, quality-score, and metric columns.
-- Old->new mappings: DATASET_ID->ID, ORGANIZATION_NAME->C_ORGANIZATION,
-- PAGE_URL->URL, NB_RESOURCES->RESOURCES_COUNT, NB_REUSES->METRIC_REUSES,
-- NB_FOLLOWERS->METRIC_FOLLOWERS, NB_VIEWS->METRIC_VIEWS.
-- Dropped (gone from publisher export): TOPIC, LAST_UPDATE, RESOURCE_*.
-- Casts kept as landed (TEXT); explicit casts happen in the mart.

with source as (

    select * from {{ source('ripple_raw', 'INTL_FR_DATA_GOUV_FULL') }}

),

renamed as (

    select
        nullif(trim("ID"), '')                       as dataset_id,
        nullif(trim("SLUG"), '')                     as slug,
        nullif(trim("TITLE"), '')                    as title,
        nullif(trim("ACRONYM"), '')                  as acronym,
        nullif(trim("DESCRIPTION"), '')              as description,
        nullif(trim("ORGANIZATION_ID"), '')          as organization_id,
        nullif(trim("C_ORGANIZATION"), '')           as organization_name,
        nullif(trim("OWNER"), '')                    as owner,
        nullif(trim("OWNER_ID"), '')                 as owner_id,
        nullif(trim("LICENSE"), '')                  as license,
        nullif(trim("FREQUENCY"), '')                as frequency,
        nullif(trim("CREATED_AT"), '')               as created_at,
        nullif(trim("LAST_MODIFIED"), '')            as last_modified,
        nullif(trim("ARCHIVED"), '')                 as archived,
        nullif(trim("FEATURED"), '')                 as featured,
        nullif(trim("RESOURCES_COUNT"), '')          as nb_resources,
        nullif(trim("RESOURCES_FORMATS"), '')        as resources_formats,
        nullif(trim("METRIC_REUSES"), '')            as nb_reuses,
        nullif(trim("METRIC_FOLLOWERS"), '')         as nb_followers,
        nullif(trim("METRIC_VIEWS"), '')             as nb_views,
        nullif(trim("METRIC_RESOURCES_DOWNLOADS"), '') as nb_resource_downloads,
        nullif(trim("QUALITY_SCORE"), '')            as quality_score,
        nullif(trim("TAGS"), '')                     as tags,
        nullif(trim("SPATIAL_GRANULARITY"), '')      as spatial_granularity,
        nullif(trim("SPATIAL_ZONES"), '')            as spatial_zones,
        nullif(trim("TEMPORAL_COVERAGE_START"), '')  as temporal_coverage_start,
        nullif(trim("TEMPORAL_COVERAGE_END"), '')    as temporal_coverage_end,
        nullif(trim("URL"), '')                      as page_url,
        nullif(trim("HARVEST_REMOTE_URL"), '')       as harvest_remote_url,
        _INGESTED_AT                                 as _loaded_at,
        'https://www.data.gouv.fr/'                  as _source_url

    from source

)

select * from renamed
qualify row_number() over (partition by dataset_id order by _loaded_at desc) = 1
