{{ config(tags=['spine_generated']) }}

-- GRAIN: one row per retraction record (RECORD_ID is the natural key; a small number
-- of duplicate RECORD_ID rows exist in the raw feed -- deduped here via qualify).
-- SPINE_ENTITY: not determined -- no registry hint available.

with source as (

    select * from {{ source('ripple_raw', 'FED_RETRACTION_WATCH') }}

),

renamed as (

    select
        RECORD_ID as record_id,
        TITLE as title,
        SUBJECT as subject,
        INSTITUTION as institution,
        JOURNAL as journal,
        PUBLISHER as publisher,
        COUNTRY as country,
        AUTHOR as author,
        URLS as urls,
        ARTICLETYPE as article_type,
        try_to_timestamp(RETRACTIONDATE, 'MM/DD/YYYY HH24:MI') as retraction_date,
        RETRACTIONDOI as retraction_doi,
        RETRACTIONPUBMEDID as retraction_pubmed_id,
        try_to_timestamp(ORIGINALPAPERDATE, 'MM/DD/YYYY HH24:MI') as original_paper_date,
        ORIGINALPAPERDOI as original_paper_doi,
        ORIGINALPAPERPUBMEDID as original_paper_pubmed_id,
        RETRACTIONNATURE as retraction_nature,
        REASON as reason,
        PAYWALLED as paywalled,
        NOTES as notes,
        INGESTED_AT as _loaded_at,
        'https://retractionwatch.com/retraction-watch-database-user-guide/' as _source_url

    from source

)

select * from renamed
qualify row_number() over (partition by record_id order by _loaded_at desc) = 1
