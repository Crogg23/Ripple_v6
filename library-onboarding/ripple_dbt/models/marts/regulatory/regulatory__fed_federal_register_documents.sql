{{ config(materialized='table') }}

with base as (

    select * from {{ ref('stg_fed_federal_register_documents__federal_register_documents') }}

),

enriched as (

    select

        -- primary key
        document_number,

        -- core identifiers for cross-source joins
        citation,
        docket_ids,
        regulation_id_numbers,
        cfr_references,
        agency_names                                                        as agency,

        -- document metadata
        title,
        type,
        subtype,
        action,
        abstract,
        excerpts,
        president,
        executive_order_notes,

        -- agency detail (raw JSON for downstream parsing)
        agencies,
        agency_names,

        -- dates
        publication_date,
        effective_on,
        comments_close_on,

        -- derived date parts for easy filtering
        year(publication_date)                                              as publication_year,
        month(publication_date)                                             as publication_month,
        date_trunc('quarter', publication_date)                             as publication_quarter,

        -- page info
        start_page,
        end_page,
        page_length,
        (end_page - start_page + 1)                                         as derived_page_count,

        -- flags
        is_significant,

        -- comment window (days open)
        datediff(
            'day',
            publication_date,
            comments_close_on
        )                                                                   as comment_window_days,

        -- days until effective
        datediff(
            'day',
            publication_date,
            effective_on
        )                                                                   as days_until_effective,

        -- urls
        html_url,
        pdf_url,
        full_text_xml_url,
        body_html_url,
        json_url,
        raw_text_url,
        images,

        -- pipeline metadata
        _ingested_at,
        _source_run_id

    from base

)

select * from enriched
