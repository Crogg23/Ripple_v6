{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'XC_RETRACTION_WATCH_DATABASE') }}

),

keyed as (

    -- RECORD_ID is NEAR-unique (71,389 distinct of 71,608 rows). The collisions
    -- are genuinely distinct records sharing an id, NOT exact dupes, so a
    -- row_number() over the full-row hash is appended as a deterministic
    -- provenance tiebreaker to make retraction_record_id fully unique.
    select
        source.*,
        trim(RECORD_ID)
            || '-'
            || row_number() over (
                   partition by RECORD_ID
                   order by hash(*)
               ) as retraction_record_id
    from source
    -- blank/trailer rows with no RECORD_ID carry no usable retraction data
    where RECORD_ID is not null and trim(RECORD_ID) <> ''

),

renamed as (

    select

        -- identifiers
        retraction_record_id,
        trim(RECORD_ID)                                as record_id,
        trim(ORIGINALPAPERDOI)                         as original_paper_doi,
        trim(ORIGINALPAPERPUBMEDID)                    as original_paper_pubmed_id,
        trim(RETRACTIONDOI)                            as retraction_doi,
        trim(RETRACTIONPUBMEDID)                       as retraction_pubmed_id,

        -- paper
        trim(TITLE)                                    as title,
        trim(SUBJECT)                                  as subjects,
        trim(INSTITUTION)                              as institutions,
        trim(JOURNAL)                                  as journal,
        trim(PUBLISHER)                                as publisher,
        trim(COUNTRY)                                  as countries,
        trim(AUTHOR)                                   as authors,
        trim(ARTICLETYPE)                              as article_types,
        trim(URLS)                                     as urls,

        -- retraction
        trim(RETRACTIONNATURE)                         as retraction_nature,
        trim(REASON)                                   as reasons,
        -- dates arrive as 'M/D/YYYY H:MM' text; keep the date part
        try_to_date(split_part(trim(RETRACTIONDATE), ' ', 1), 'MM/DD/YYYY')
                                                       as retraction_date,
        try_to_date(split_part(trim(ORIGINALPAPERDATE), ' ', 1), 'MM/DD/YYYY')
                                                       as original_paper_date,
        trim(PAYWALLED)                                as paywalled,
        trim(NOTES)                                    as notes,

        -- UNNAMED_20 (all-null junk column) intentionally dropped

        -- metadata (INGESTED_AT is a NUMBER epoch in microseconds)
        to_timestamp_ntz(INGESTED_AT, 6)               as _loaded_at,
        SOURCE_RUN_ID                                  as _source_run_id,
        SRC_SHA256                                     as _src_sha256

    from keyed

)

select * from renamed
