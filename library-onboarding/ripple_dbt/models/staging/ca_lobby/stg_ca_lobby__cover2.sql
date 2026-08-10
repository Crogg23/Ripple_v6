{{ config(materialized='view') }}

/*
  Generated 2026-08-09 (73-source backlog, wave 2b) from live-verified specs.
  CAL-ACCESS lobbying cover-page entity lines: one row per entity line item on a filing version (filing_id + amend_id + line_item unique).
  Grain: one row = one entity line on a filing version.
*/

with source as (
    select * from {{ source('ripple_raw', 'CA_LOBBY_COVER2') }}
),

renamed as (
    select
        nullif(trim(AMEND_ID), '')                                     as amend_id,
        nullif(trim(ENTITY_CD), '')                                    as entity_cd,
        nullif(trim(ENTITY_ID), '')                                    as entity_id,
        nullif(trim(ENTY_NAMF), '')                                    as enty_namf,
        nullif(trim(ENTY_NAML), '')                                    as enty_naml,
        nullif(trim(ENTY_NAMS), '')                                    as enty_nams,
        nullif(trim(ENTY_NAMT), '')                                    as enty_namt,
        nullif(trim(ENTY_TITLE), '')                                   as enty_title,
        nullif(trim(FILING_ID), '')                                    as filing_id,
        nullif(trim(FORM_TYPE), '')                                    as form_type,
        nullif(trim(LINE_ITEM), '')                                    as line_item,
        nullif(trim(REC_TYPE), '')                                     as rec_type,
        nullif(trim(TRAN_ID), '')                                      as tran_id,
        to_timestamp_ntz(INGESTED_AT, 6)                               as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                                as _source_run_id
    from source
)

select * from renamed
