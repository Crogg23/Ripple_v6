{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'XC_BIORXIV_MEDRXIV') }}

),

renamed_cast as (

    select

        -- ---------------------------------------------------------------
        -- Key identifiers
        -- ---------------------------------------------------------------
        doi                                                        as doi,
        biorxiv_doi                                                as biorxiv_doi,
        published_doi                                              as published_doi,
        author_corresponding                                       as person_name,
        funding_id                                                 as funder_ror_id,

        -- ---------------------------------------------------------------
        -- Preprint core fields
        -- ---------------------------------------------------------------
        title                                                      as title,
        authors                                                    as authors,
        author_corresponding_institution                           as author_corresponding_institution,
        try_to_date(date)                                          as preprint_posted_date,
        version                                                    as version,
        type                                                       as submission_type,
        license                                                    as license,
        category                                                   as category,
        jats_xml_path                                              as jats_xml_path,
        abstract                                                   as abstract,
        published                                                  as published_journal_doi_raw,
        server                                                     as server,

        -- ---------------------------------------------------------------
        -- Funding fields
        -- ---------------------------------------------------------------
        funding_name                                               as funding_name,
        funding_id_type                                            as funding_id_type,
        funding_award                                              as funding_award,

        -- ---------------------------------------------------------------
        -- Publication-link fields  (pubs / pub endpoints)
        -- ---------------------------------------------------------------
        published_journal                                          as published_journal,
        preprint_platform                                          as preprint_platform,
        preprint_title                                             as preprint_title,
        preprint_authors                                           as preprint_authors,
        preprint_category                                          as preprint_category,
        try_to_date(preprint_date)                                 as preprint_date,
        try_to_date(published_date)                                as published_date,
        preprint_abstract                                          as preprint_abstract,
        preprint_author_corresponding                              as preprint_author_corresponding,
        preprint_author_corresponding_institution                  as preprint_author_corresponding_institution,

        -- ---------------------------------------------------------------
        -- Summary-statistics fields
        -- ---------------------------------------------------------------
        month                                                      as stat_month,
        try_to_number(new_papers)                                  as new_papers,
        try_to_number(new_papers_cumulative)                       as new_papers_cumulative,
        try_to_number(revised_papers)                              as revised_papers,
        try_to_number(revised_papers_cumulative)                   as revised_papers_cumulative,

        -- ---------------------------------------------------------------
        -- Usage-statistics fields
        -- ---------------------------------------------------------------
        try_to_number(abstract_views)                              as abstract_views,
        try_to_number(full_text_views)                             as full_text_views,
        try_to_number(pdf_downloads)                               as pdf_downloads,
        try_to_number(abstract_cumulative)                         as abstract_cumulative,
        try_to_number(full_text_cumulative)                        as full_text_cumulative,
        try_to_number(pdf_cumulative)                              as pdf_cumulative,

        -- ---------------------------------------------------------------
        -- Metadata
        -- ---------------------------------------------------------------
        _ingested_at                                               as _ingested_at,
        _source_run_id                                             as _source_run_id

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by doi, biorxiv_doi, published_doi, person_name, funder_ror_id, stat_month
            order by _ingested_at desc
        ) as _row_num
    from renamed_cast

)

select * exclude (_row_num)
from deduped
where _row_num = 1
