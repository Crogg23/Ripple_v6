{{ config(materialized='view') }}

/*
  Staging for CFPB Consumer Complaints (incremental / append-only landing).
  Casts TEXT -> typed values, normalises Yes/No + True/False flags to booleans,
  and deduplicates on complaint_id keeping the most-recently-ingested record.

  2026-07-28 fix: this model was written against the CFPB API's snake_case field
  names (complaint_id, date_received, timely, complaint_what_happened, ...), but
  the raw table was reloaded on 07-23 via CFPB's bulk CSV export instead, which
  uses the human-readable CSV headers below (spaces, mixed case, one has a '?') --
  none of the old unquoted references resolved against these, so the mart had
  been silently stuck on a stale 500-row build ever since (the view itself
  errored on a bare SELECT * the moment anything tried to rebuild it). Also:
  _INGESTED_AT is now a native TIMESTAMP_NTZ, not the epoch-microseconds NUMBER
  the old to_timestamp_ntz(_ingested_at, 6) cast expected -- referenced directly.
  A tiny number of rows (3 of 17,179,788, confirmed live) have a CSV-escaping
  glitch that shifts "Timely response?" into a numeric complaint-ID-shaped
  value; is_timely is cast defensively so those become NULL, not garbage.
*/

with source as (

    select * from {{ source('ripple_raw', 'FED_CFPB_COMPLAINTS') }}

),

renamed_cast as (

    select

        -- primary key
        trim("Complaint ID")                                   as complaint_id,

        -- dates (source values are ISO-8601 strings; keep the calendar date)
        try_to_date(left(trim("Date received"), 10))          as date_received,
        try_to_date(left(trim("Date sent to company"), 10))   as date_sent_to_company,

        -- complaint taxonomy
        nullif(trim("Product"), '')                           as product,
        nullif(trim("Sub-product"), '')                       as sub_product,
        nullif(trim("Issue"), '')                             as issue,
        nullif(trim("Sub-issue"), '')                         as sub_issue,

        -- company + geography (cross-source join keys)
        nullif(trim("Company"), '')                           as company,
        nullif(trim("State"), '')                             as state,
        nullif(trim("ZIP code"), '')                          as zip_code,

        -- intake + outcome
        nullif(trim("Submitted via"), '')                     as submitted_via,
        nullif(trim("Company response to consumer"), '')      as company_response,
        nullif(trim("Company public response"), '')           as company_public_response,
        case trim("Timely response?")
            when 'Yes' then true
            when 'No' then false
            -- else NULL: covers the handful of CSV-escaping-shifted rows too
        end                                                    as is_timely,
        nullif(trim("Consumer complaint narrative"), '') is not null
                                                               as has_narrative,
        nullif(trim("Tags"), '')                              as tags,
        nullif(trim("Consumer complaint narrative"), '')      as complaint_narrative,

        -- pipeline audit columns
        _INGESTED_AT                                          as _ingested_at,
        nullif(trim(_SOURCE_RUN_ID), '')                      as _source_run_id

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by complaint_id
            order by _ingested_at desc nulls last
        ) as _row_num
    from renamed_cast

)

select
    complaint_id,
    date_received,
    date_sent_to_company,
    product,
    sub_product,
    issue,
    sub_issue,
    company,
    state,
    zip_code,
    submitted_via,
    company_response,
    company_public_response,
    is_timely,
    has_narrative,
    tags,
    complaint_narrative,
    _ingested_at,
    _source_run_id
from deduped
-- complaint_id is not null: excludes the 1 remaining row (of the 3 known
-- CSV-escaping-shifted raw rows, 2026-07-28) whose Complaint ID landed empty
-- after the shift -- a complaint record with no ID has no analytical value,
-- and its other fields are already misaligned from the same glitch.
where _row_num = 1
  and complaint_id is not null
