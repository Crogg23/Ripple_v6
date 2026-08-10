{{ config(materialized='view') }}

/*
  Hand-built 2026-08-09 (73-source backlog, wave 2). Retraction Watch
  database (via Crossref): retracted/corrected scholarly papers with reasons.
  Grain: one row = one retraction/correction record. RECORD_ID is blank on
  214 rows as published; every non-blank RECORD_ID is unique (71,377).
  Dates are M/D/YYYY H:MM strings.
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_RETRACTION_WATCH') }}
),

renamed as (
    select
        nullif(trim(RECORD_ID), '')                             as record_id,
        nullif(trim(TITLE), '')                                 as title,
        nullif(trim(SUBJECT), '')                               as subjects,
        nullif(trim(INSTITUTION), '')                           as institutions,
        nullif(trim(JOURNAL), '')                               as journal,
        nullif(trim(PUBLISHER), '')                             as publisher,
        nullif(trim(COUNTRY), '')                               as countries,
        nullif(trim(AUTHOR), '')                                as authors,
        nullif(trim(URLS), '')                                  as urls,
        nullif(trim(ARTICLETYPE), '')                           as article_type,
        try_to_date(split_part(nullif(trim(RETRACTIONDATE), ''), ' ', 1), 'MM/DD/YYYY')    as retraction_date,
        nullif(trim(RETRACTIONDOI), '')                         as retraction_doi,
        nullif(trim(RETRACTIONPUBMEDID), '')                    as retraction_pubmed_id,
        try_to_date(split_part(nullif(trim(ORIGINALPAPERDATE), ''), ' ', 1), 'MM/DD/YYYY') as original_paper_date,
        nullif(trim(ORIGINALPAPERDOI), '')                      as original_paper_doi,
        nullif(trim(ORIGINALPAPERPUBMEDID), '')                 as original_paper_pubmed_id,
        nullif(trim(RETRACTIONNATURE), '')                      as retraction_nature,
        nullif(trim(REASON), '')                                as reasons,
        nullif(trim(PAYWALLED), '')                             as paywalled,
        nullif(trim(NOTES), '')                                 as notes,
        to_timestamp_ntz(INGESTED_AT, 6)                        as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                         as _source_run_id
    from source
)

select * from renamed
