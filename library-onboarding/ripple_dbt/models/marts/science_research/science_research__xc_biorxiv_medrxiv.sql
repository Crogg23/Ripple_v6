{{ config(materialized='table') }}

with base as (

    select * from {{ ref('stg_xc_biorxiv_medrxiv__preprint_manuscript') }}

)

select

    -- ---------------------------------------------------------------
    -- Key identifiers  (exposed for cross-source joins)
    -- ---------------------------------------------------------------
    doi,
    biorxiv_doi,
    published_doi,
    person_name,
    funder_ror_id,

    -- ---------------------------------------------------------------
    -- Preprint descriptors
    -- ---------------------------------------------------------------
    title,
    authors,
    author_corresponding_institution,
    preprint_posted_date,
    version,
    submission_type,
    license,
    category,
    abstract,
    server,
    jats_xml_path,

    -- ---------------------------------------------------------------
    -- Funding
    -- ---------------------------------------------------------------
    funding_name,
    funding_id_type,
    funding_award,

    -- ---------------------------------------------------------------
    -- Journal-publication link
    -- ---------------------------------------------------------------
    published_journal_doi_raw,
    published_journal,
    preprint_platform,
    preprint_title,
    preprint_authors,
    preprint_category,
    preprint_date,
    published_date,
    preprint_abstract,
    preprint_author_corresponding,
    preprint_author_corresponding_institution,

    -- ---------------------------------------------------------------
    -- Derived convenience flags
    -- ---------------------------------------------------------------
    case
        when published_doi is not null or published_journal_doi_raw is not null
        then true
        else false
    end                                                            as is_published,

    datediff(
        'day',
        coalesce(preprint_date, preprint_posted_date),
        published_date
    )                                                              as days_preprint_to_publication,

    -- ---------------------------------------------------------------
    -- Summary statistics
    -- ---------------------------------------------------------------
    stat_month,
    new_papers,
    new_papers_cumulative,
    revised_papers,
    revised_papers_cumulative,

    -- ---------------------------------------------------------------
    -- Usage statistics
    -- ---------------------------------------------------------------
    abstract_views,
    full_text_views,
    pdf_downloads,
    abstract_cumulative,
    full_text_cumulative,
    pdf_cumulative,

    -- ---------------------------------------------------------------
    -- Metadata
    -- ---------------------------------------------------------------
    _ingested_at,
    _source_run_id

from base
