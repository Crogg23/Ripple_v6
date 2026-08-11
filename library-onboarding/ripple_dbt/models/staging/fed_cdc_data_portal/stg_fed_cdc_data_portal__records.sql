{{ config(tags=['minimal_staging']) }}

-- GRAIN: one row per CDC dataset (RESOURCE_ID unique — the Socrata 4x4 id).
-- Re-pulled in full 2026-08-11 into FED_CDC_DATA_PORTAL_FULL (1,471 rows).
-- SCHEMA CHANGE: the full pull is the portal's dataset CATALOG, not the old
-- capped indicator-observation sample. INDICATOR / YEAR / STATE / VALUE /
-- UNIT / DATA_VALUE_TYPE are gone, and so are the always-null synthetic
-- FIPS / ZIP_CODE columns flagged by the dead-ID triage.

with source as (

    select * from {{ source('ripple_raw', 'FED_CDC_DATA_PORTAL_FULL') }}

),

renamed as (

    select
        nullif(trim(RESOURCE_ID), '')                  as dataset_id,
        nullif(trim(RESOURCE_NAME), '')                as dataset_name,
        nullif(trim(RESOURCE_DESCRIPTION), '')         as description,
        nullif(trim(RESOURCE_TYPE), '')                as resource_type,
        nullif(trim(RESOURCE_PARENT_FXF), '')          as parent_dataset_id,
        nullif(trim(RESOURCE_ATTRIBUTION), '')         as attribution,
        nullif(trim(RESOURCE_ATTRIBUTION_LINK), '')    as attribution_link,
        nullif(trim(RESOURCE_CONTACT_EMAIL), '')       as contact_email,
        nullif(trim(RESOURCE_PROVENANCE), '')          as provenance,
        nullif(trim(RESOURCE_CREATEDAT), '')           as created_at,
        nullif(trim(RESOURCE_UPDATEDAT), '')           as updated_at,
        nullif(trim(RESOURCE_DATA_UPDATED_AT), '')     as data_updated_at,
        nullif(trim(RESOURCE_METADATA_UPDATED_AT), '') as metadata_updated_at,
        nullif(trim(RESOURCE_PUBLICATION_DATE), '')    as publication_date,
        nullif(trim(RESOURCE_PAGE_VIEWS), '')          as page_views,
        nullif(trim(RESOURCE_DOWNLOAD_COUNT), '')      as download_count,
        nullif(trim(CATEGORIES), '')                   as categories,
        nullif(trim(DOMAIN_CATEGORY), '')              as domain_category,
        nullif(trim(DOMAIN_TAGS), '')                  as domain_tags,
        nullif(trim(OWNER_DISPLAY_NAME), '')           as owner_display_name,
        nullif(trim(PERMALINK), '')                    as permalink,
        nullif(trim(LINK), '')                         as link,
        _INGESTED_AT                                   as _loaded_at,
        'https://data.cdc.gov/'                        as _source_url

    from source

)

select * from renamed
