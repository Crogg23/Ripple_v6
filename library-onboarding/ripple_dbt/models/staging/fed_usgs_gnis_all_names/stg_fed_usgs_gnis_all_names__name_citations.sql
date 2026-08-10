{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_USGS_GNIS_ALL_NAMES') }}

),

renamed as (

    select

        -- identifiers
        trim(FEATURE_ID)                               as feature_id,

        -- dimensions
        trim(FEATURE_NAME)                             as feature_name,
        trim(FEATURE_NAME_OFFICIAL)                    as feature_name_official,
        SOURCECITATIONABBREVIATION                     as source_citation_abbreviation,
        trim(SOURCEORIGINATOR)                         as source_originator,
        trim(SOURCEREFTYPE)                            as source_ref_type,
        trim(TITLE)                                    as title,
        trim(EDITION)                                  as edition,
        trim(SOURCEURL)                                as source_url,
        try_to_date(trim(PUBLICATIONDATE))             as publication_date,
        trim(SERIESNAME)                               as series_name,
        trim(SERIESISSUE)                              as series_issue,
        try_to_date(trim(ENDING_DATE))                 as ending_date,
        try_to_date(trim(DATE_CREATED))                as date_created,
        trim(CITATION)                                 as citation,

        -- metadata
        INGESTED_AT                                    as ingested_at,
        SOURCE_RUN_ID                                  as source_run_id,
        SRC_SHA256                                     as src_sha256

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by feature_id, feature_name, citation
            order by ingested_at desc
        ) as _row_num
    from renamed
    where feature_id is not null

)

select
    {{ dbt_utils.generate_surrogate_key(['feature_id', 'feature_name', 'citation']) }} as name_citation_id,
    feature_id,
    feature_name,
    feature_name_official,
    source_citation_abbreviation,
    source_originator,
    source_ref_type,
    title,
    edition,
    source_url,
    publication_date,
    series_name,
    series_issue,
    ending_date,
    date_created,
    citation,
    ingested_at,
    source_run_id,
    src_sha256
from deduped
where _row_num = 1
