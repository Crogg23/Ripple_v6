{{ config(materialized='view') }}

/*
  Generated 2026-08-09 (73-source backlog, wave 2b) from live-verified specs.
  IRS Form 8871 related entities of 527 orgs: one row per related entity per form (form_id + entity_id unique).
  Grain: one row = one related-entity listing.
*/

with source as (
    select * from {{ source('ripple_raw', 'IRS527_RELATED_ENTITIES') }}
),

renamed as (
    select
        nullif(trim(FORM_ID_NUMBER), '')                               as form_id_number,
        nullif(trim(ENTITY_ID), '')                                    as entity_id,
        nullif(trim(ORG_NAME), '')                                     as org_name,
        nullif(trim(EIN), '')                                          as ein,
        nullif(trim(ENTITY_NAME), '')                                  as entity_name,
        nullif(trim(ENTITY_RELATIONSHIP), '')                          as entity_relationship,
        nullif(trim(ENTITY_ADDR1), '')                                 as entity_addr1,
        nullif(trim(ENTITY_ADDR2), '')                                 as entity_addr2,
        nullif(trim(ENTITY_CITY), '')                                  as entity_city,
        nullif(trim(ENTITY_STATE), '')                                 as entity_state,
        nullif(trim(ENTITY_ZIP), '')                                   as entity_zip,
        nullif(trim(ENTITY_ZIP_EXT), '')                               as entity_zip_ext,
        to_timestamp_ntz(INGESTED_AT, 6)                               as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                                as _source_run_id
    from source
)

select * from renamed
