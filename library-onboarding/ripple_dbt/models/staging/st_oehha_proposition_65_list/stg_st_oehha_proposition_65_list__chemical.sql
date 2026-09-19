{{ config(materialized='view') }}

-- HAND-EDITED 2026-09-19: dedupe is a whole-raw-row hash (_row_hash), see the
-- comment in deduped. The staging generator skips files carrying this marker.

with source as (

    -- _row_hash: hash of every landing column except the load stamps
    select *, hash(* exclude (_INGESTED_AT, _SOURCE_RUN_ID, _SRC_SHA256)) as _row_hash
    from {{ source('ripple_raw', 'ST_OEHHA_PROPOSITION_65_LIST') }}

),

renamed as (

    select

        -- key identifiers
        trim(CHEMICAL)                                      as chemical,
        trim(CAS_NO)                                        as cas_no,

        -- attributes
        trim(TYPE_OF_TOXICITY)                              as type_of_toxicity,
        trim(LISTING_MECHANISM)                             as listing_mechanism,
        -- 2026-08-09 fix: landed values are ISO (e.g. '1990-01-01'); the old
        -- 'MM/DD/YYYY' format string nulled out 100% of dates.
        try_to_date(trim(DATE_LISTED))                      as date_listed,
        try_to_double(trim(NSRL_OR_MADL_G_DAY_A))          as nsrl_or_madl_g_day,

        -- overflow / extra columns retained as-is
        trim(COL_6)                                         as col_6,
        trim(COL_7)                                         as col_7,
        trim(COL_8)                                         as col_8,

        -- pipeline metadata
        _ingested_at,
        _source_run_id,

        -- whole-raw-row hash, carried for the dedupe + surrogate key only
        _row_hash

    from source
    where CHEMICAL is not null
      and trim(CHEMICAL) != ''

),

deduped as (

    -- 2026-09-19: the old partition was (chemical, cas_no). It hid 69 of 1,021
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
    -- surrogate key
    -- 2026-09-19: _row_hash added so the key stays one-per-row now that
    -- (chemical, cas_no) repeats in the output.
    {{ dbt_utils.generate_surrogate_key(['chemical', 'cas_no', '_row_hash']) }} as chemical_key,

    chemical,
    cas_no,
    type_of_toxicity,
    listing_mechanism,
    date_listed,
    nsrl_or_madl_g_day,
    col_6,
    col_7,
    col_8,
    _ingested_at,
    _source_run_id

from deduped
where _row_num = 1
