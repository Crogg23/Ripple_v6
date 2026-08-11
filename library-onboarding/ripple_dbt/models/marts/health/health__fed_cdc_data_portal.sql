{{ config(materialized='table', schema='HEALTH') }}

-- Source: CDC Open Data Portal (data.cdc.gov), 1,471 rows
-- (re-pulled in full 2026-08-11). SCHEMA CHANGE: the full pull is the
-- portal's dataset CATALOG (one row per dataset, dataset_id unique) — the
-- old capped table's indicator-observation columns are gone, and the two
-- synthetic always-null columns (FIPS, ZIP_CODE) flagged by the dead-ID
-- triage are dropped with them.
-- Date formats sampled 2026-08-11: all timestamps are ISO
-- 'YYYY-MM-DDTHH:MI:SS.FF3Z' — parsed with an explicit format on left(19).

with base as (
    select * from {{ ref('stg_fed_cdc_data_portal__records') }}
)

select
    dataset_id,
    dataset_name,
    description,
    resource_type,
    parent_dataset_id,
    attribution,
    provenance,
    try_to_timestamp_ntz(left(created_at, 19), 'YYYY-MM-DD"T"HH24:MI:SS')
                                                   as created_at,
    try_to_timestamp_ntz(left(updated_at, 19), 'YYYY-MM-DD"T"HH24:MI:SS')
                                                   as updated_at,
    try_to_timestamp_ntz(left(data_updated_at, 19), 'YYYY-MM-DD"T"HH24:MI:SS')
                                                   as data_updated_at,
    try_to_timestamp_ntz(left(metadata_updated_at, 19), 'YYYY-MM-DD"T"HH24:MI:SS')
                                                   as metadata_updated_at,
    try_to_date(left(publication_date, 10), 'YYYY-MM-DD')
                                                   as publication_date,
    try_to_number(page_views)                      as page_views,
    try_to_number(download_count)                  as download_count,
    categories,
    domain_category,
    domain_tags,
    owner_display_name,
    permalink,
    link
from base
