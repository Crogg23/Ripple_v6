{{ config(materialized='table') }}

with base as (

    select * from {{ ref('stg_fed_wpa_slave_narratives__slave_narratives') }}

),

final as (

    select

        -- primary key
        loc_item_id,

        -- key identifiers for cross-source joins
        person_name,
        interview_date,
        state_fips,
        state,

        -- derived / convenience columns
        year(interview_date)                                as interview_year,
        month(interview_date)                               as interview_month,

        -- narrative content
        title,
        interviewer,
        document_type,
        format_label,
        subjects,
        full_text,
        length(full_text)                                   as full_text_char_length,

        -- digital access
        digital_url,
        thumbnail_url,

        -- source provenance
        'fed_wpa_slave_narratives'                          as source_id,
        _ingested_at,
        _source_run_id

    from base

)

select * from final
