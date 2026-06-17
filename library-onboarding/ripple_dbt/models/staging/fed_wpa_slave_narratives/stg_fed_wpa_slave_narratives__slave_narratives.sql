{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'FED_WPA_SLAVE_NARRATIVES') }}

),

renamed as (

    select

        -- identifiers
        loc_item_id                                         as loc_item_id,
        trim(person_name)                                   as person_name,
        trim(state_fips)                                    as state_fips,
        trim(state)                                         as state,

        -- dates
        try_to_date(interview_date, 'YYYY-MM-DD')           as interview_date,

        -- descriptive text
        trim(title)                                         as title,
        trim(interviewer)                                   as interviewer,
        trim(document_type)                                 as document_type,
        trim(format_label)                                  as format_label,
        trim(subjects)                                      as subjects,
        trim(full_text)                                     as full_text,

        -- urls
        trim(digital_url)                                   as digital_url,
        trim(thumbnail_url)                                 as thumbnail_url,

        -- metadata
        current_timestamp()                                 as _ingested_at,
        cast(null as varchar)                               as _source_run_id

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by loc_item_id
            order by interview_date nulls last
        ) as _row_num
    from renamed

)

select
    loc_item_id,
    person_name,
    state_fips,
    state,
    interview_date,
    title,
    interviewer,
    document_type,
    format_label,
    subjects,
    full_text,
    digital_url,
    thumbnail_url,
    _ingested_at,
    _source_run_id

from deduped
where _row_num = 1
