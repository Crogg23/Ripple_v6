{{ config(materialized='table', schema='OPEN_DATA') }}

-- Source: data.gouv.fr, 130,431 rows (re-pulled in full 2026-08-11; the old
-- capped table held 2,765 dataset+resource rows). SCHEMA CHANGE with the full
-- pull: publisher export is now DATASET-grain — resource-level columns are
-- gone; owner, archived, quality-score and download metrics are new.
-- Date formats sampled 2026-08-11: CREATED_AT / LAST_MODIFIED are ISO
-- timestamps ('YYYY-MM-DDTHH:MI:SS[.FF6]'), temporal coverage is 'YYYY-MM-DD'.

with base as (
    select * from {{ ref('stg_intl_fr_data_gouv__records') }}
)

select
    dataset_id,
    slug,
    title,
    acronym,
    description,
    organization_id,
    organization_name,
    owner,
    owner_id,
    license,
    frequency,
    try_to_timestamp_ntz(left(created_at, 19), 'YYYY-MM-DD"T"HH24:MI:SS')
                                                   as created_at,
    try_to_timestamp_ntz(left(last_modified, 19), 'YYYY-MM-DD"T"HH24:MI:SS')
                                                   as last_modified,
    archived,
    try_to_number(nb_resources)                    as nb_resources,
    resources_formats,
    try_to_number(nb_reuses)                       as nb_reuses,
    try_to_number(nb_followers)                    as nb_followers,
    try_to_number(nb_views)                        as nb_views,
    try_to_number(nb_resource_downloads)           as nb_resource_downloads,
    try_to_double(quality_score)                   as quality_score,
    tags,
    spatial_granularity,
    spatial_zones,
    try_to_date(left(temporal_coverage_start, 10), 'YYYY-MM-DD')
                                                   as temporal_coverage_start,
    try_to_date(left(temporal_coverage_end, 10), 'YYYY-MM-DD')
                                                   as temporal_coverage_end,
    page_url,
    harvest_remote_url
from base
