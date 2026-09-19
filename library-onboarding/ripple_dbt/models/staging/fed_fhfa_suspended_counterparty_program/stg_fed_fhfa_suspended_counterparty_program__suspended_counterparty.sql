{{ config(materialized='view') }}

-- HAND-EDITED 2026-09-19: dedupe is a whole-raw-row hash (_row_hash), see the
-- comment in deduped. The staging generator skips files carrying this marker.

with source as (

    -- _row_hash: hash of every landing column except the load stamps
    select *, hash(* exclude (_INGESTED_AT, _SOURCE_RUN_ID, _SRC_SHA256)) as _row_hash
    from {{ source('ripple_raw', 'FED_FHFA_SUSPENDED_COUNTERPARTY_PROGRAM') }}

),

renamed as (

    select
        -- identifiers
        LAST_NAME                                          as last_name,
        COMPANY                                            as company,

        -- descriptive fields
        FIRST_NAME                                         as first_name,
        CITY                                               as city,
        STATE                                              as state,

        -- dates
        try_to_date(EFFECTIVE_DATESORT_ASCENDING)          as effective_date,
        try_to_date(SUSPENSION_END_DATE)                   as suspension_end_date,

        -- other fields
        SUSPENSION_ORDER                                   as suspension_order,

        -- metadata
        _ingested_at,
        _source_run_id,

        -- whole-raw-row hash, carried for the dedupe only
        _row_hash

    from source

),

deduped as (

    -- 2026-09-19: the old partition was (last_name, company). It hid 19 of 241
    -- landing rows on a single load -- that pair does not identify a row. The
    -- dedupe is now the whole-raw-row hash, so only exact copies are dropped
    -- (0 exact copies in landing).
    select *,
        row_number() over (
            partition by _row_hash
            order by _ingested_at desc
        ) as _row_num
    from renamed

)

select
    last_name,
    company,
    first_name,
    city,
    state,
    effective_date,
    suspension_end_date,
    suspension_order,
    _ingested_at,
    _source_run_id
from deduped
where _row_num = 1
