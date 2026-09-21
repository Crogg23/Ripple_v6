{{ config(materialized='view') }}

-- HAND-EDITED 2026-09-19: dedupe is a whole-raw-row hash (_row_hash), see the
-- comment in deduped. The staging generator skips files carrying this marker.

with source as (

    -- _row_hash: hash of every landing column except the load stamps. This
    -- model never reads the landing stamps (it fabricates _ingested_at below),
    -- but the table carries them: landing_clean__fed_fdic_enforcement reads
    -- "_INGESTED_AT".
    select *, hash(* exclude (_INGESTED_AT, _SOURCE_RUN_ID, _SRC_SHA256)) as _row_hash
    from {{ source('ripple_raw', 'FED_FDIC_ENFORCEMENT') }}

),

renamed as (

    select
        -- raw fields
        RAW_TEXT                                          as raw_text,
        ORDER_URL                                         as order_url,

        -- parsed / typed fields extracted from raw_text
        -- 2026-09-21: the four casts below carry the stg_int / stg_date guards inline; the regex argument has both
        -- quote kinds and a backslash, which a Jinja string cannot hold.
        -- FDIC certificate number (numeric identifier for the institution)
        iff(regexp_like(nullif(trim(regexp_substr(RAW_TEXT, '"fdic_cert_number"\s*:\s*"([^"]+)"', 1, 1, 'e', 1)), ''), '[+-]?[0-9]+([.]0+)?'), try_to_number(nullif(trim(regexp_substr(RAW_TEXT, '"fdic_cert_number"\s*:\s*"([^"]+)"', 1, 1, 'e', 1)), ''), 38, 0), null
        )                                                 as fdic_cert_number,

        -- company_id mirrors fdic_cert_number for cross-source keying
        iff(regexp_like(nullif(trim(regexp_substr(RAW_TEXT, '"fdic_cert_number"\s*:\s*"([^"]+)"', 1, 1, 'e', 1)), ''), '[+-]?[0-9]+([.]0+)?'), try_to_number(nullif(trim(regexp_substr(RAW_TEXT, '"fdic_cert_number"\s*:\s*"([^"]+)"', 1, 1, 'e', 1)), ''), 38, 0), null
        )                                                 as company_id,

        -- docket number
        nullif(trim(regexp_substr(RAW_TEXT, '"docket_number"\s*:\s*"([^"]+)"', 1, 1, 'e', 1)), '')
                                                          as docket_number,

        -- respondent / person name
        nullif(trim(regexp_substr(RAW_TEXT, '"respondent_name"\s*:\s*"([^"]+)"', 1, 1, 'e', 1)), '')
                                                          as respondent_name,

        nullif(trim(regexp_substr(RAW_TEXT, '"person_name"\s*:\s*"([^"]+)"', 1, 1, 'e', 1)), '')
                                                          as person_name,

        -- NMLS ID
        nullif(trim(regexp_substr(RAW_TEXT, '"nmls_id"\s*:\s*"([^"]+)"', 1, 1, 'e', 1)), '')
                                                          as nmls_id,

        -- effective / order date
        iff(regexp_like(nullif(trim(regexp_substr(RAW_TEXT, '"date"\s*:\s*"([^"]+)"', 1, 1, 'e', 1)), ''), '.*[0-9A-Za-z][-/][0-9A-Za-z].*'), try_to_date(nullif(trim(regexp_substr(RAW_TEXT, '"date"\s*:\s*"([^"]+)"', 1, 1, 'e', 1)), '')), null
        )                                                 as date,

        -- additional descriptive fields
        nullif(trim(regexp_substr(RAW_TEXT, '"action_type"\s*:\s*"([^"]+)"', 1, 1, 'e', 1)), '')
                                                          as action_type,

        nullif(trim(regexp_substr(RAW_TEXT, '"institution_name"\s*:\s*"([^"]+)"', 1, 1, 'e', 1)), '')
                                                          as institution_name,

        nullif(trim(regexp_substr(RAW_TEXT, '"city"\s*:\s*"([^"]+)"', 1, 1, 'e', 1)), '')
                                                          as city,

        nullif(trim(regexp_substr(RAW_TEXT, '"state"\s*:\s*"([^"]+)"', 1, 1, 'e', 1)), '')
                                                          as state,

        nullif(trim(regexp_substr(RAW_TEXT, '"termination_date"\s*:\s*"([^"]+)"', 1, 1, 'e', 1)), '')
                                                          as termination_date_raw,

        iff(regexp_like(nullif(trim(regexp_substr(RAW_TEXT, '"termination_date"\s*:\s*"([^"]+)"', 1, 1, 'e', 1)), ''), '.*[0-9A-Za-z][-/][0-9A-Za-z].*'), try_to_date(nullif(trim(regexp_substr(RAW_TEXT, '"termination_date"\s*:\s*"([^"]+)"', 1, 1, 'e', 1)), '')), null
        )                                                 as termination_date,

        -- ingestion metadata
        current_timestamp()                               as _ingested_at,
        null::varchar                                     as _source_run_id,

        -- whole-raw-row hash, carried for the dedupe only
        _row_hash

    from source

),

deduped as (

    -- 2026-09-19: the old partition was (docket_number, fdic_cert_number,
    -- coalesce(person_name, respondent_name)). It hid 13 of 14 landing rows on
    -- a single load -- those columns do not identify a row. The dedupe is now
    -- the whole-raw-row hash, so only exact copies are dropped (0 exact copies
    -- in landing).
    select * exclude (_row_hash)
    from renamed
    qualify row_number() over (
        partition by _row_hash
        order by _ingested_at desc
    ) = 1

)

select * from deduped
