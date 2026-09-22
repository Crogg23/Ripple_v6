-- KEY WIDENED 2026-09-22 (row sweep): document_number alone hid 9 rows.
-- A corrected notice is re-published under the same number on a later date with its own citation.
{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'FED_FEDERAL_REGISTER_DOCUMENTS') }}

),

renamed as (

    select

        -- primary key
        document_number                                         as document_number,

        -- descriptive fields
        title                                                   as title,
        type                                                    as type,
        abstract                                                as abstract,
        action                                                  as action,
        subtype                                                 as subtype,
        president                                               as president,
        excerpts                                                as excerpts,
        executive_order_notes                                   as executive_order_notes,

        -- agency fields
        agencies                                                as agencies,
        agency_names                                            as agency_names,

        -- dates
        {{ stg_date('publication_date') }}                           as publication_date,
        {{ stg_date('effective_on') }}                               as effective_on,
        {{ stg_date('comments_close_on') }}                          as comments_close_on,

        -- citation / identifiers
        citation                                                as citation,
        docket_ids                                              as docket_ids,
        regulation_id_numbers                                   as regulation_id_numbers,
        cfr_references                                          as cfr_references,

        -- page references
        {{ stg_int('start_page') }}                               as start_page,
        {{ stg_int('end_page') }}                                 as end_page,
        {{ stg_int('page_length') }}                              as page_length,

        -- flags
        case
            when lower(significant) in ('true', '1', 'yes') then true
            when lower(significant) in ('false', '0', 'no') then false
            else null
        end                                                     as is_significant,

        -- urls
        html_url                                                as html_url,
        pdf_url                                                 as pdf_url,
        full_text_xml_url                                       as full_text_xml_url,
        body_html_url                                           as body_html_url,
        json_url                                                as json_url,
        raw_text_url                                            as raw_text_url,
        images                                                  as images,

        -- metadata
        _ingested_at                                            as _ingested_at,
        _source_run_id                                          as _source_run_id

    from source

),

deduped as (

    select *
    from (
        select
            *,
            row_number() over (
                partition by document_number, publication_date
                order by _ingested_at desc
            ) as _row_num
        from renamed
    )
    where _row_num = 1

)

select
    document_number,
    title,
    type,
    abstract,
    action,
    subtype,
    president,
    excerpts,
    executive_order_notes,
    agencies,
    agency_names,
    publication_date,
    effective_on,
    comments_close_on,
    citation,
    docket_ids,
    regulation_id_numbers,
    cfr_references,
    start_page,
    end_page,
    page_length,
    is_significant,
    html_url,
    pdf_url,
    full_text_xml_url,
    body_html_url,
    json_url,
    raw_text_url,
    images,
    _ingested_at,
    _source_run_id
from deduped
